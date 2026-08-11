# Model Card: VARI OS Predictive Risk Engine

## Model Details
* **Model Type:** Logistic Regression
* **Task:** Binary Classification (Imminent Critical Risk Prediction)
* **Version:** 1.0.0
* **Framework:** scikit-learn

## Intended Use
* **Primary Use Case:** Forecasting probability of crowd and environmental stress for the Vari Pilgrimage prototype.
* **Non-Intended Use:** This model MUST NOT be used for real-world emergency management. It does NOT predict exact incidents, and it is NOT a flood/hydrodynamic simulator.

## Training Data
* **Source:** Synthetic Data Generator (`src/data_generator.py`)
* **WARNING:** The data is completely synthetic. It encodes illustrative rules mapping density, temperature, and water to future risk, with controlled noise. 

## Features
* `crowd_density`: Percentage utilization of capacity (0-1).
* `temperature_c`: Celsius.
* `humidity_pct`: Percentage (0-1).
* `water_availability_pct`: Percentage of reserves (0-1).
* `hour_of_day`: Integer (0-23).
* `zone_id`: Categorical.

## Target
* **`critical_risk_30m` / `critical_risk_60m`**: A binary label representing whether a mathematical `Stress_Index` will exceed a critical threshold within the horizon. 

## Metrics
* Evaluated via: Accuracy, Precision, Recall, F1-Score, ROC-AUC.
* Test set evaluates models on chronologically held-out data to verify prevention of temporal data leakage. 

## Ethical / Safety Limitations
* This model makes assumptions about human crowd dynamics that have not been validated. 
* Predictions are probabilistic and may have high false-positive or false-negative rates depending on synthetic noise parameters.
* **Production Requirements:** A real deployment would require massive real-time CCTV, IoT sensor integration, and rigorous re-training with historically validated Wari datasets.
