import pandas as pd
import joblib
import os
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

def evaluate(model_path, X_test, y_test, horizon):
    model = joblib.load(model_path)
    
    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': accuracy_score(y_test, preds),
        'precision': precision_score(y_test, preds, zero_division=0),
        'recall': recall_score(y_test, preds, zero_division=0),
        'f1': f1_score(y_test, preds, zero_division=0),
        'roc_auc': roc_auc_score(y_test, probs)
    }
    
    cm = confusion_matrix(y_test, preds)
    return metrics, cm

def main():
    os.makedirs("../reports", exist_ok=True)
    
    test_df = pd.read_csv("../data/processed/test.csv")
    
    with open("../models/model_metadata.json", "r") as f:
        metadata = json.load(f)
        
    features = metadata['features']
    X_test = test_df[features]
    
    metrics_30m, cm_30m = evaluate("../models/risk_model_30m.joblib", X_test, test_df['critical_risk_30m'], 30)
    metrics_60m, cm_60m = evaluate("../models/risk_model_60m.joblib", X_test, test_df['critical_risk_60m'], 60)
    
    report_content = f"""# VARI OS - Predictive Risk Engine Evaluation Report

> [!WARNING]
> **Synthetic Data Disclaimer**
> This model was trained and evaluated on synthetically generated data for hackathon prototyping. The relationships and coefficients are illustrative and are not derived from real Wari operational data. Do not fabricate real-world performance.

## Overview
This report details the genuine test-set metrics for the selected predictive models. The test set represents the final 15% of the chronological synthetic dataset, ensuring no future data leakage.

## Test Set Metrics (30-Minute Horizon)
**Model Type:** {metadata['models']['30m']['model_type']}
**Target:** `critical_risk_30m`

*   **Accuracy:** {metrics_30m['accuracy']:.4f}
*   **Precision:** {metrics_30m['precision']:.4f}
*   **Recall:** {metrics_30m['recall']:.4f}
*   **F1-Score:** {metrics_30m['f1']:.4f}
*   **ROC-AUC:** {metrics_30m['roc_auc']:.4f}

### Confusion Matrix (30m)
| | Predicted Negative (0) | Predicted Positive (1) |
|---|---|---|
| **Actual Negative (0)** | {cm_30m[0,0]} | {cm_30m[0,1]} |
| **Actual Positive (1)** | {cm_30m[1,0]} | {cm_30m[1,1]} |

---

## Test Set Metrics (60-Minute Horizon)
**Model Type:** {metadata['models']['60m']['model_type']}
**Target:** `critical_risk_60m`

*   **Accuracy:** {metrics_60m['accuracy']:.4f}
*   **Precision:** {metrics_60m['precision']:.4f}
*   **Recall:** {metrics_60m['recall']:.4f}
*   **F1-Score:** {metrics_60m['f1']:.4f}
*   **ROC-AUC:** {metrics_60m['roc_auc']:.4f}

### Confusion Matrix (60m)
| | Predicted Negative (0) | Predicted Positive (1) |
|---|---|---|
| **Actual Negative (0)** | {cm_60m[0,0]} | {cm_60m[0,1]} |
| **Actual Positive (1)** | {cm_60m[1,0]} | {cm_60m[1,1]} |
"""

    with open("../reports/evaluation_report.md", "w") as f:
        f.write(report_content)
        
    print("Evaluation complete. Report saved to reports/evaluation_report.md")

if __name__ == "__main__":
    main()
