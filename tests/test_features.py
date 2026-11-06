"""
Unit Tests for Feature Engineering Module.
"""

import pandas as pd
import numpy as np
import pytest

from src.feature_engineering import engineer_features


def test_delivery_delay_calculation():
    """Verify delivery delay and is_delayed flag."""
    df = pd.DataFrame({
        "Actual_Delivery_Days": [8, 5, 10],
        "Expected_Delivery_Days": [5, 5, 12],
        "Previous_Returns": [1, 2, 0],
        "Previous_Orders": [10, 5, 20],
        "Product_Price_INR": [1000.0, 2000.0, 5000.0],
        "Discount_Percent": [10.0, 20.0, 0.0]
    })
    res = engineer_features(df)

    assert "delivery_delay" in res.columns
    assert "is_delayed" in res.columns
    assert res["delivery_delay"].tolist() == [3, 0, -2]
    assert res["is_delayed"].tolist() == [1, 0, 0]


def test_customer_return_frequency():
    """Verify customer return frequency ratio."""
    df = pd.DataFrame({
        "Actual_Delivery_Days": [5],
        "Expected_Delivery_Days": [5],
        "Previous_Returns": [3],
        "Previous_Orders": [12],
        "Product_Price_INR": [1000.0],
        "Discount_Percent": [10.0]
    })
    res = engineer_features(df)
    assert "customer_return_frequency" in res.columns
    assert np.isclose(res["customer_return_frequency"].iloc[0], 3 / 12)


def test_effective_price_calculation():
    """Verify effective price after discount."""
    df = pd.DataFrame({
        "Actual_Delivery_Days": [5],
        "Expected_Delivery_Days": [5],
        "Previous_Returns": [0],
        "Previous_Orders": [5],
        "Product_Price_INR": [10000.0],
        "Discount_Percent": [25.0]
    })
    res = engineer_features(df)
    assert np.isclose(res["effective_price"].iloc[0], 7500.0)
