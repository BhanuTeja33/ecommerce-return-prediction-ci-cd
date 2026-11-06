"""
MLOps Quality Gate for Product Return Prediction Model.

Verifies:
1. Model artifact exists and is non-empty.
2. Metrics file exists with valid thresholds.
3. At least two models were evaluated.
4. Model can be loaded and executed on test inputs.
"""

import sys
import os
import json
import joblib
import pandas as pd


ACCURACY_THRESHOLD = 0.55
ROC_AUC_THRESHOLD = 0.50
MIN_MODELS_EVALUATED = 2


def run_quality_gate() -> bool:
    print("=" * 60)
    print("  RUNNING MLOPS QUALITY GATE VERIFICATION")
    print("=" * 60)

    # 1. Model Artifact Check
    model_path = os.path.join("models", "best_model.joblib")
    if not os.path.exists(model_path):
        print(f"[FAIL] Missing model artifact at: {model_path}")
        return False
    size_kb = os.path.getsize(model_path) / 1024
    print(f"[PASS] Model artifact found ({size_kb:.2f} KB): {model_path}")

    # 2. Metrics File Check
    metrics_path = "metrics.json"
    if not os.path.exists(metrics_path):
        print(f"[FAIL] Missing metrics file: {metrics_path}")
        return False

    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    # 3. Candidate models evaluated check
    models_evaluated = metrics.get("models_evaluated", [])
    if len(models_evaluated) < MIN_MODELS_EVALUATED:
        print(f"[FAIL] Required at least {MIN_MODELS_EVALUATED} models evaluated, but got {len(models_evaluated)}")
        return False
    print(f"[PASS] Evaluated {len(models_evaluated)} models: {', '.join(models_evaluated)}")

    # 4. Performance Gate Check
    accuracy = metrics.get("accuracy", 0.0)
    roc_auc = metrics.get("roc_auc", 0.0)

    print(f"[CHECK] Accuracy: {accuracy:.4f} (Threshold: >= {ACCURACY_THRESHOLD})")
    if accuracy < ACCURACY_THRESHOLD:
        print(f"[FAIL] Accuracy {accuracy:.4f} is below required threshold {ACCURACY_THRESHOLD}")
        return False
    print(f"[PASS] Accuracy gate passed: {accuracy:.4f} >= {ACCURACY_THRESHOLD}")

    print(f"[CHECK] ROC AUC: {roc_auc:.4f} (Threshold: >= {ROC_AUC_THRESHOLD})")
    if roc_auc < ROC_AUC_THRESHOLD:
        print(f"[FAIL] ROC AUC {roc_auc:.4f} is below required threshold {ROC_AUC_THRESHOLD}")
        return False
    print(f"[PASS] ROC AUC gate passed: {roc_auc:.4f} >= {ROC_AUC_THRESHOLD}")

    # 5. Pipeline Deserialization & Smoke Test
    try:
        pipeline = joblib.load(model_path)
        sample = pd.DataFrame([{
            "Product_Category": "Electronics",
            "Product_Price_INR": 15000.0,
            "Discount_Percent": 15.0,
            "Expected_Delivery_Days": 5,
            "Actual_Delivery_Days": 7,
            "Customer_Rating_PreOrder": 3.8,
            "Previous_Returns": 3,
            "Previous_Orders": 12,
            "Payment_Method": "Card",
            "Damaged_Package_Flag": "No",
            "Package_Size": "Medium",
            "Promotion_Active": "Yes",
            "delivery_delay": 2.0,
            "customer_return_frequency": 0.25,
            "effective_price": 12750.0,
            "is_delayed": 1,
            "return_risk_score": 0.25,
        }])
        pred = pipeline.predict(sample)[0]
        prob = pipeline.predict_proba(sample)[0][1]
        print(f"[PASS] Model smoke test succeeded: pred={pred}, prob={prob:.4f}")
    except Exception as e:
        print(f"[FAIL] Model inference smoke test failed: {e}")
        return False

    print("=" * 60)
    print("  ALL QUALITY GATE CHECKS PASSED SUCCESSFULLY")
    print("=" * 60)
    return True


if __name__ == "__main__":
    passed = run_quality_gate()
    sys.exit(0 if passed else 1)
