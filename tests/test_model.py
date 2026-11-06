"""
Unit Tests for Trained Model Pipeline.
"""

import os
import joblib
import pandas as pd
import pytest


def test_model_artifact_exists():
    """Verify serialized model artifact exists."""
    path = os.path.join("models", "best_model.joblib")
    assert os.path.exists(path), f"Missing model artifact at {path}"


def test_model_inference_output():
    """Verify loaded model can predict on sample input with valid probabilities."""
    path = os.path.join("models", "best_model.joblib")
    pipeline = joblib.load(path)

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

    pred = pipeline.predict(sample)
    prob = pipeline.predict_proba(sample)

    assert len(pred) == 1
    assert pred[0] in [0, 1]
    assert 0.0 <= prob[0][1] <= 1.0
