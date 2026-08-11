import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_synthetic_data(num_days=14, interval_minutes=5, seed=42):
    """
    Generates synthetic dataset for Vari OS predictive risk engine.
    Applies chronological dynamics and calculates future risk targets.
    """
    np.random.seed(seed)
    
    # 1. Generate base timeline
    start_date = datetime(2026, 7, 1) # Arbitrary start date for the Wari
    intervals_per_day = (24 * 60) // interval_minutes
    total_intervals = num_days * intervals_per_day
    
    timestamps = [start_date + timedelta(minutes=i*interval_minutes) for i in range(total_intervals)]
    
    zones = [f"Z{i}" for i in range(1, 21)] # 20 zones
    
    data = []
    
    # Simulation parameters per zone (add some static variance)
    zone_base_density = {z: np.random.uniform(0.1, 0.4) for z in zones}
    
    for t in timestamps:
        hour = t.hour
        
        # Diurnal temperature cycle: peaks at 14:00 (2 PM)
        # Base temp 25, peak 45. Shifted sine wave.
        temp_cycle = 35 + 10 * np.sin((hour - 8) * np.pi / 12)
        base_temp = np.clip(temp_cycle + np.random.normal(0, 1), 25, 45)
        
        # Humidity usually inverse to temp
        base_humidity = np.clip(1.0 - (base_temp - 20) * 0.02 + np.random.normal(0, 0.05), 0.1, 1.0)
        
        for z in zones:
            # Crowd dynamics based on hour
            # Surges in morning (6-9) and evening (16-19)
            if 6 <= hour <= 9 or 16 <= hour <= 19:
                crowd_surge = np.random.uniform(0.3, 0.6)
            else:
                crowd_surge = np.random.uniform(0.0, 0.2)
                
            density = np.clip(zone_base_density[z] + crowd_surge + np.random.normal(0, 0.1), 0.0, 1.0)
            
            # Water availability depletes with time and heat, gets restocked periodically
            # We'll simulate a random walk with periodic jumps (restocks)
            water = np.random.uniform(0.2, 1.0) # simplified for now
            
            data.append({
                'timestamp': t,
                'zone_id': z,
                'crowd_density': density,
                'temperature_c': base_temp + np.random.normal(0, 0.5), # local zone variation
                'humidity_pct': base_humidity + np.random.normal(0, 0.02),
                'water_availability_pct': water
            })
            
    df = pd.DataFrame(data)
    
    # 2. Simulate future states and calculate targets
    print("Simulating future states...")
    
    # Sort by zone and time to easily get future states using shift
    df = df.sort_values(['zone_id', 'timestamp']).reset_index(drop=True)
    
    # 30 min = 6 intervals, 60 min = 12 intervals (at 5 min intervals)
    steps_30m = 30 // interval_minutes
    steps_60m = 60 // interval_minutes
    
    # For a realistic simulation, the *actual* future state would involve adding noise
    # Since we already have the chronological data, we can just look ahead,
    # and add a little bit of "unpredictable event" noise to represent reality vs perfect knowledge.
    
    # Look ahead
    df['future_density_30m'] = df.groupby('zone_id')['crowd_density'].shift(-steps_30m)
    df['future_temp_30m'] = df.groupby('zone_id')['temperature_c'].shift(-steps_30m)
    df['future_water_30m'] = df.groupby('zone_id')['water_availability_pct'].shift(-steps_30m)
    
    df['future_density_60m'] = df.groupby('zone_id')['crowd_density'].shift(-steps_60m)
    df['future_temp_60m'] = df.groupby('zone_id')['temperature_c'].shift(-steps_60m)
    df['future_water_60m'] = df.groupby('zone_id')['water_availability_pct'].shift(-steps_60m)
    
    # Drop rows at the end of the timeline that don't have future states
    df = df.dropna().copy()
    
    # Calculate stress index
    # Stress_Index = (0.5 * future_density) + (0.3 * normalized_temp) + (0.2 * (1 - future_water))
    def calc_stress(density, temp, water):
        norm_temp = (temp - 25) / 20.0 # scale 25-45 to 0-1
        norm_temp = np.clip(norm_temp, 0.0, 1.0)
        return (0.5 * density) + (0.3 * norm_temp) + (0.2 * (1.0 - water))
        
    df['stress_30m'] = calc_stress(df['future_density_30m'], df['future_temp_30m'], df['future_water_30m'])
    df['stress_60m'] = calc_stress(df['future_density_60m'], df['future_temp_60m'], df['future_water_60m'])
    
    # Target assignment
    CRITICAL_THRESHOLD = 0.80
    
    df['critical_risk_30m'] = (df['stress_30m'] > CRITICAL_THRESHOLD).astype(int)
    df['critical_risk_60m'] = (df['stress_60m'] > CRITICAL_THRESHOLD).astype(int)
    
    # Label Noise: randomly flip 3% of labels
    flip_mask_30m = np.random.rand(len(df)) < 0.03
    df.loc[flip_mask_30m, 'critical_risk_30m'] = 1 - df.loc[flip_mask_30m, 'critical_risk_30m']
    
    flip_mask_60m = np.random.rand(len(df)) < 0.03
    df.loc[flip_mask_60m, 'critical_risk_60m'] = 1 - df.loc[flip_mask_60m, 'critical_risk_60m']
    
    # 3. Add derived features
    df['hour_of_day'] = df['timestamp'].dt.hour
    
    # 4. Data Leakage Prevention - Drop future columns
    columns_to_drop = [
        'future_density_30m', 'future_temp_30m', 'future_water_30m', 'stress_30m',
        'future_density_60m', 'future_temp_60m', 'future_water_60m', 'stress_60m'
    ]
    df = df.drop(columns=columns_to_drop)
    
    # 5. Temporal Split (70/15/15)
    print("Splitting data temporally...")
    df = df.sort_values('timestamp').reset_index(drop=True)
    
    n_total = len(df)
    train_end = int(n_total * 0.70)
    val_end = int(n_total * 0.85)
    
    df_train = df.iloc[:train_end].copy()
    df_val = df.iloc[train_end:val_end].copy()
    df_test = df.iloc[val_end:].copy()
    
    # Drop timestamp from splits (we only use hour_of_day for modeling)
    df_train = df_train.drop(columns=['timestamp'])
    df_val = df_val.drop(columns=['timestamp'])
    df_test = df_test.drop(columns=['timestamp'])
    
    return df_train, df_val, df_test

if __name__ == "__main__":
    import os
    os.makedirs("../data/processed", exist_ok=True)
    
    print("Generating synthetic data...")
    df_train, df_val, df_test = generate_synthetic_data(num_days=14, interval_minutes=5)
    
    print(f"Train shape: {df_train.shape}")
    print(f"Val shape: {df_val.shape}")
    print(f"Test shape: {df_test.shape}")
    print(f"Target 30m positive rate (train): {df_train['critical_risk_30m'].mean():.2f}")
    
    df_train.to_csv("../data/processed/train.csv", index=False)
    df_val.to_csv("../data/processed/validation.csv", index=False)
    df_test.to_csv("../data/processed/test.csv", index=False)
    print("Saved to ../data/processed/")
