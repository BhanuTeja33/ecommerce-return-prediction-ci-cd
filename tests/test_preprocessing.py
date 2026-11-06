"""
Unit Tests for Data Preprocessing Module.
"""

import pandas as pd
import numpy as np
import pytest

from src.data_preprocessing import clean_invalid_values, handle_missing_values, compute_imputation_statistics


def test_clean_negative_prices():
    """Negative or zero product prices should be converted to NaN."""
    df = pd.DataFrame({
        "Product_Price_INR": [-200.0, 0.0, 1500.0],
        "Discount_Percent": [10.0, 20.0, 30.0]
    })
    cleaned = clean_invalid_values(df)
    assert np.isnan(cleaned["Product_Price_INR"].iloc[0])
    assert np.isnan(cleaned["Product_Price_INR"].iloc[1])
    assert cleaned["Product_Price_INR"].iloc[2] == 1500.0


def test_clean_out_of_range_discounts():
    """Discounts outside [0, 100] should be converted to NaN."""
    df = pd.DataFrame({
        "Product_Price_INR": [1000.0, 2000.0, 3000.0],
        "Discount_Percent": [-5.0, 125.0, 25.0]
    })
    cleaned = clean_invalid_values(df)
    assert np.isnan(cleaned["Discount_Percent"].iloc[0])
    assert np.isnan(cleaned["Discount_Percent"].iloc[1])
    assert cleaned["Discount_Percent"].iloc[2] == 25.0


def test_imputation_replaces_all_nans():
    """Missing values should be completely imputed."""
    df = pd.DataFrame({
        "Product_Price_INR": [np.nan, 2000.0, 3000.0],
        "Discount_Percent": [10.0, np.nan, 30.0],
        "Expected_Delivery_Days": [5, 6, 7],
        "Actual_Delivery_Days": [np.nan, 8, 9],
        "Customer_Rating_PreOrder": [np.nan, 4.0, 4.5],
        "Payment_Method": [np.nan, "COD", "Card"]
    })
    cleaned, stats = handle_missing_values(df)
    assert cleaned["Product_Price_INR"].isnull().sum() == 0
    assert cleaned["Discount_Percent"].isnull().sum() == 0
    assert cleaned["Actual_Delivery_Days"].isnull().sum() == 0
    assert cleaned["Customer_Rating_PreOrder"].isnull().sum() == 0
    assert cleaned["Payment_Method"].isnull().sum() == 0
