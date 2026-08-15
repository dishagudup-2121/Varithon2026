import os
import sys
import pandas as pd
import logging
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error
import joblib

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def evaluate_persistence(df_test):
    """
    Persistence baseline: prediction(E, T+H) = load(E, T)
    """
    y_true = df_test['target_load_t_plus_h']
    y_pred = df_test['current_load']
    
    mae = mean_absolute_error(y_true, y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)
    return mae, rmse

def train_and_evaluate(df_train, df_val, df_test, feature_cols, target_col):
    X_train = df_train[feature_cols]
    y_train = df_train[target_col]
    X_test = df_test[feature_cols]
    y_test = df_test[target_col]
    
    # 1. Evaluate Persistence
    baseline_mae, baseline_rmse = evaluate_persistence(df_test)
    logger.info("=== PERSISTENCE BASELINE ===")
    logger.info(f"MAE:  {baseline_mae:.4f}")
    logger.info(f"RMSE: {baseline_rmse:.4f}")
    
    # 2. Linear Regression
    logger.info("\n=== LINEAR REGRESSION ===")
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)
    lr_mae = mean_absolute_error(y_test, lr_pred)
    lr_rmse = root_mean_squared_error(y_test, lr_pred)
    logger.info(f"MAE:  {lr_mae:.4f}")
    logger.info(f"RMSE: {lr_rmse:.4f}")
    
    # 3. Random Forest
    logger.info("\n=== RANDOM FOREST ===")
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_rmse = root_mean_squared_error(y_test, rf_pred)
    logger.info(f"MAE:  {rf_mae:.4f}")
    logger.info(f"RMSE: {rf_rmse:.4f}")
    
    # 4. Comparison Gate
    logger.info("\n=== COMPARISON GATE ===")
    candidates = {
        "Persistence": {"mae": baseline_mae, "model": None},
        "Linear Regression": {"mae": lr_mae, "model": lr_model},
        "Random Forest": {"mae": rf_mae, "model": rf_model}
    }
    
    best_name = min(candidates, key=lambda k: candidates[k]["mae"])
    best_mae = candidates[best_name]["mae"]
    
    if best_name == "Persistence":
        logger.warning(f"No ML model beats persistence (Baseline MAE: {baseline_mae:.4f}).")
        logger.error("STOPPING ML DEPLOYMENT. The baseline remains superior.")
        sys.exit(1)
        
    logger.info(f"WINNER: {best_name} (MAE: {best_mae:.4f}) beat persistence (MAE: {baseline_mae:.4f}).")
    
    # 5. Serialization
    model_dir = os.path.join(os.path.dirname(__file__), '../../models')
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, 'edge_load_model.joblib')
    joblib.dump(candidates[best_name]["model"], model_path)
    logger.info(f"Successfully serialized {best_name} to {model_path}.")
    
    # Store metadata about the model
    import json
    meta_path = os.path.join(model_dir, 'edge_load_metadata.json')
    metadata = {
        "model_identifier": "absolute_edge_load",
        "model_version": best_name.lower().replace(" ", "_") + "_v1",
        "features": feature_cols,
        "test_mae": float(best_mae),
        "baseline_mae": float(baseline_mae)
    }
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)
        
    logger.info(f"Metadata saved to {meta_path}")
    
def main():
    data_path = os.path.join(os.path.dirname(__file__), '../../data/processed/phase3_dataset.csv')
    if not os.path.exists(data_path):
        logger.error(f"Dataset not found at {data_path}. Run phase3_generate_dataset.py first.")
        sys.exit(1)
        
    df = pd.read_csv(data_path)
    logger.info(f"Loaded {len(df)} rows from dataset.")
    
    # Sort chronologically just to be absolutely certain
    df = df.sort_values(by=["tick", "edge_id"]).reset_index(drop=True)
    
    unique_ticks = df['tick'].unique()
    num_ticks = len(unique_ticks)
    
    train_idx = int(num_ticks * 0.6)
    val_idx = int(num_ticks * 0.8)
    
    train_ticks = unique_ticks[:train_idx]
    val_ticks = unique_ticks[train_idx:val_idx]
    test_ticks = unique_ticks[val_idx:]
    
    df_train = df[df['tick'].isin(train_ticks)]
    df_val = df[df['tick'].isin(val_ticks)]
    df_test = df[df['tick'].isin(test_ticks)]
    
    logger.info(f"Chronological Split applied:")
    logger.info(f"Train: {len(df_train)} rows (Ticks {train_ticks[0]} to {train_ticks[-1]})")
    logger.info(f"Val:   {len(df_val)} rows (Ticks {val_ticks[0]} to {val_ticks[-1]})")
    logger.info(f"Test:  {len(df_test)} rows (Ticks {test_ticks[0]} to {test_ticks[-1]})")
    
    feature_cols = [
        "current_load", 
        "load_t_minus_1", 
        "load_t_minus_5", 
        "load_t_minus_15",
        "absolute_load_change_1",
        "absolute_load_change_5",
        "absolute_load_change_15",
        "consecutive_occupied_ticks"
    ]
    target_col = "target_load_t_plus_h"
    
    train_and_evaluate(df_train, df_val, df_test, feature_cols, target_col)

if __name__ == "__main__":
    main()
