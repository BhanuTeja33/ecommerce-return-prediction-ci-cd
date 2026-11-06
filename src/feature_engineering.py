"""
Feature Engineering Module for E-Commerce Product Return Prediction.

Creates domain-specific features:
- delivery_delay: Difference between actual delivery and expected delivery days
- customer_return_frequency: Ratio of previous returns to previous orders
- effective_price: Net product price after applying discount percentage
- is_delayed: Binary indicator flag if actual delivery exceeded expected delivery
- return_risk_score: Combined risk signal from package condition and return history
"""

import pandas as pd
import numpy as np


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies feature engineering transformations to the input DataFrame.
    """
    data = df.copy()

    # 1. Delivery delay (days)
    if "Actual_Delivery_Days" in data.columns and "Expected_Delivery_Days" in data.columns:
        data["delivery_delay"] = data["Actual_Delivery_Days"] - data["Expected_Delivery_Days"]
        data["is_delayed"] = (data["delivery_delay"] > 0).astype(int)
    else:
        data["delivery_delay"] = 0.0
        data["is_delayed"] = 0

    # 2. Customer return frequency (ratio of returns to total orders)
    if "Previous_Returns" in data.columns and "Previous_Orders" in data.columns:
        # Avoid division by zero
        orders = np.maximum(data["Previous_Orders"].values, 1.0)
        data["customer_return_frequency"] = np.clip(data["Previous_Returns"].values / orders, 0.0, 1.0)
    else:
        data["customer_return_frequency"] = 0.0

    # 3. Effective purchase price (in INR)
    if "Product_Price_INR" in data.columns and "Discount_Percent" in data.columns:
        discount_factor = 1.0 - (data["Discount_Percent"] / 100.0)
        data["effective_price"] = np.maximum(data["Product_Price_INR"] * discount_factor, 0.0)
    else:
        data["effective_price"] = data.get("Product_Price_INR", 0.0)

    # 4. Damaged package indicator (numeric binary)
    if "Damaged_Package_Flag" in data.columns:
        damaged_num = (data["Damaged_Package_Flag"].astype(str).str.lower() == "yes").astype(int)
    else:
        damaged_num = 0

    # 5. High return risk signal (combining return frequency and damaged package)
    data["return_risk_score"] = (
        (data["customer_return_frequency"] > 0.25).astype(int) * 0.6
        + damaged_num * 0.4
    )

    return data
