"""
Data Preprocessing Module for E-Commerce Product Return Prediction.

Handles:
- Missing value detection and imputation
- Invalid value correction (negative prices, out-of-range discounts)
- Data type consistency
"""

from typing import Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np


def clean_invalid_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans domain-specific invalid values from the dataset:
    - Product_Price_INR <= 0 is invalid (negative or zero prices).
    - Discount_Percent < 0 or > 100 is invalid.
    - Customer_Rating_PreOrder < 1 or > 5 is clamped or set to NaN.
    """
    cleaned = df.copy()

    if "Product_Price_INR" in cleaned.columns:
        invalid_price_mask = cleaned["Product_Price_INR"] <= 0
        cleaned.loc[invalid_price_mask, "Product_Price_INR"] = np.nan

    if "Discount_Percent" in cleaned.columns:
        invalid_discount_mask = (cleaned["Discount_Percent"] < 0) | (cleaned["Discount_Percent"] > 100)
        cleaned.loc[invalid_discount_mask, "Discount_Percent"] = np.nan

    if "Customer_Rating_PreOrder" in cleaned.columns:
        invalid_rating_mask = (cleaned["Customer_Rating_PreOrder"] < 1.0) | (cleaned["Customer_Rating_PreOrder"] > 5.0)
        cleaned.loc[invalid_rating_mask, "Customer_Rating_PreOrder"] = np.nan

    return cleaned


def compute_imputation_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes baseline imputation statistics from the training dataset.
    """
    cleaned = clean_invalid_values(df)
    stats: Dict[str, Any] = {
        "price_median": float(cleaned["Product_Price_INR"].median()),
        "discount_median": float(cleaned["Discount_Percent"].median()),
        "rating_median": float(cleaned["Customer_Rating_PreOrder"].median()),
        "payment_mode": str(cleaned["Payment_Method"].dropna().mode()[0]) if "Payment_Method" in cleaned.columns else "Card",
        "expected_delivery_median": float(cleaned["Expected_Delivery_Days"].median()) if "Expected_Delivery_Days" in cleaned.columns else 7.0,
        "actual_delivery_median": float(cleaned["Actual_Delivery_Days"].median()) if "Actual_Delivery_Days" in cleaned.columns else 8.0,
    }
    return stats


def handle_missing_values(
    df: pd.DataFrame, stats: Optional[Dict[str, Any]] = None
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Imputes missing values using provided or computed statistics.
    """
    cleaned = clean_invalid_values(df)

    if stats is None:
        stats = compute_imputation_statistics(cleaned)

    if "Product_Price_INR" in cleaned.columns:
        cleaned["Product_Price_INR"] = cleaned["Product_Price_INR"].fillna(stats["price_median"])

    if "Discount_Percent" in cleaned.columns:
        cleaned["Discount_Percent"] = cleaned["Discount_Percent"].fillna(stats["discount_median"])

    if "Customer_Rating_PreOrder" in cleaned.columns:
        cleaned["Customer_Rating_PreOrder"] = cleaned["Customer_Rating_PreOrder"].fillna(stats["rating_median"])

    if "Payment_Method" in cleaned.columns:
        cleaned["Payment_Method"] = cleaned["Payment_Method"].fillna(stats["payment_mode"])

    if "Actual_Delivery_Days" in cleaned.columns:
        if "Expected_Delivery_Days" in cleaned.columns:
            cleaned["Actual_Delivery_Days"] = cleaned["Actual_Delivery_Days"].fillna(cleaned["Expected_Delivery_Days"])
        else:
            cleaned["Actual_Delivery_Days"] = cleaned["Actual_Delivery_Days"].fillna(stats["actual_delivery_median"])

    return cleaned, stats
