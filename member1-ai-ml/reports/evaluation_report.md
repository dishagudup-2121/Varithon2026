# VARI OS - Predictive Risk Engine Evaluation Report

> [!WARNING]
> **Synthetic Data Disclaimer**
> This model was trained and evaluated on synthetically generated data for hackathon prototyping. The relationships and coefficients are illustrative and are not derived from real Wari operational data. Do not fabricate real-world performance.

## Overview
This report details the genuine test-set metrics for the selected predictive models. The test set represents the final 15% of the chronological synthetic dataset, ensuring no future data leakage.

## Test Set Metrics (30-Minute Horizon)
**Model Type:** Logistic Regression
**Target:** `critical_risk_30m`

*   **Accuracy:** 0.9577
*   **Precision:** 0.0000
*   **Recall:** 0.0000
*   **F1-Score:** 0.0000
*   **ROC-AUC:** 0.6352

### Confusion Matrix (30m)
| | Predicted Negative (0) | Predicted Positive (1) |
|---|---|---|
| **Actual Negative (0)** | 11550 | 0 |
| **Actual Positive (1)** | 510 | 0 |

---

## Test Set Metrics (60-Minute Horizon)
**Model Type:** Logistic Regression
**Target:** `critical_risk_60m`

*   **Accuracy:** 0.9588
*   **Precision:** 0.0000
*   **Recall:** 0.0000
*   **F1-Score:** 0.0000
*   **ROC-AUC:** 0.6442

### Confusion Matrix (60m)
| | Predicted Negative (0) | Predicted Positive (1) |
|---|---|---|
| **Actual Negative (0)** | 11563 | 0 |
| **Actual Positive (1)** | 497 | 0 |
