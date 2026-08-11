import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
import joblib
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def load_data():
    train = pd.pd.read_csv("../data/processed/train.csv")
    val = pd.read_csv("../data/processed/validation.csv")
    return train, val

def train_and_evaluate(X_train, y_train, X_val, y_val, target_name):
    print(f"\n--- Training models for {target_name} ---")
    
    categorical_features = ['zone_id']
    numerical_features = ['crowd_density', 'temperature_c', 'humidity_pct', 'water_availability_pct', 'hour_of_day']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
        
    # Model 1: Logistic Regression
    lr_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                  ('classifier', LogisticRegression(max_iter=1000, random_state=42))])
    
    lr_pipeline.fit(X_train, y_train)
    lr_preds = lr_pipeline.predict(X_val)
    lr_probs = lr_pipeline.predict_proba(X_val)[:, 1]
    
    lr_metrics = {
        'accuracy': accuracy_score(y_val, lr_preds),
        'precision': precision_score(y_val, lr_preds, zero_division=0),
        'recall': recall_score(y_val, lr_preds, zero_division=0),
        'f1': f1_score(y_val, lr_preds, zero_division=0),
        'roc_auc': roc_auc_score(y_val, lr_probs)
    }
    
    print("Logistic Regression Val Metrics:")
    for k, v in lr_metrics.items(): print(f"  {k}: {v:.4f}")

    # Model 2: XGBoost
    xgb_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                                   ('classifier', XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42))])
    
    xgb_pipeline.fit(X_train, y_train)
    xgb_preds = xgb_pipeline.predict(X_val)
    xgb_probs = xgb_pipeline.predict_proba(X_val)[:, 1]
    
    xgb_metrics = {
        'accuracy': accuracy_score(y_val, xgb_preds),
        'precision': precision_score(y_val, xgb_preds, zero_division=0),
        'recall': recall_score(y_val, xgb_preds, zero_division=0),
        'f1': f1_score(y_val, xgb_preds, zero_division=0),
        'roc_auc': roc_auc_score(y_val, xgb_probs)
    }
    
    print("XGBoost Val Metrics:")
    for k, v in xgb_metrics.items(): print(f"  {k}: {v:.4f}")

    # Selection Logic: If XGBoost is significantly better (>0.02 ROC-AUC), pick it. 
    # Otherwise prefer Logistic Regression for interpretability.
    if (xgb_metrics['roc_auc'] - lr_metrics['roc_auc']) > 0.02:
        print(f"-> Selected XGBoost for {target_name} (better performance).")
        return xgb_pipeline, "XGBoost", xgb_metrics
    else:
        print(f"-> Selected Logistic Regression for {target_name} (comparable performance, better interpretability).")
        return lr_pipeline, "Logistic Regression", lr_metrics

def main():
    os.makedirs("../models", exist_ok=True)
    
    # We will use pandas, wait, I made a typo in load_data `pd.pd.read_csv`, let me fix it in the script below
    train = pd.read_csv("../data/processed/train.csv")
    val = pd.read_csv("../data/processed/validation.csv")
    
    features = ['zone_id', 'crowd_density', 'temperature_c', 'humidity_pct', 'water_availability_pct', 'hour_of_day']
    
    X_train = train[features]
    X_val = val[features]
    
    # Train 30m model
    model_30m, type_30m, metrics_30m = train_and_evaluate(X_train, train['critical_risk_30m'], X_val, val['critical_risk_30m'], 'critical_risk_30m')
    
    # Train 60m model
    model_60m, type_60m, metrics_60m = train_and_evaluate(X_train, train['critical_risk_60m'], X_val, val['critical_risk_60m'], 'critical_risk_60m')
    
    # Save models
    joblib.dump(model_30m, "../models/risk_model_30m.joblib")
    joblib.dump(model_60m, "../models/risk_model_60m.joblib")
    
    # Save metadata
    metadata = {
        "model_version": "v1.0.0",
        "training_timestamp": datetime.now().isoformat(),
        "dataset_version": "synthetic_v1",
        "features": features,
        "models": {
            "30m": {
                "target": "critical_risk_30m",
                "model_type": type_30m,
                "val_roc_auc": metrics_30m['roc_auc']
            },
            "60m": {
                "target": "critical_risk_60m",
                "model_type": type_60m,
                "val_roc_auc": metrics_60m['roc_auc']
            }
        },
        "assumptions": [
            "Trained and evaluated on synthetically generated data for hackathon prototyping.",
            "The relationships and coefficients are illustrative and are not derived from real Wari operational data."
        ]
    }
    
    with open("../models/model_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print("\nModels and metadata saved successfully.")

if __name__ == "__main__":
    main()
