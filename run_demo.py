"""
Simulation script to test FastAPI and Docker container endpoints.
Sends diverse sample orders and displays formatted predictions.
"""

import time
import requests
import json

BASE_URL = "http://localhost:8000"

SAMPLE_ORDERS = [
    {
        "Order_ID": "ECOM00004",
        "Product_Category": "Electronics",
        "Product_Price_INR": 22055.97,
        "Discount_Percent": 21.6,
        "Expected_Delivery_Days": 9,
        "Actual_Delivery_Days": 12,
        "Customer_Rating_PreOrder": 4.4,
        "Previous_Returns": 4,
        "Previous_Orders": 12,
        "Payment_Method": "Card",
        "Damaged_Package_Flag": "Yes",
        "Package_Size": "Large",
        "Promotion_Active": "Yes"
    },
    {
        "Order_ID": "ECOM00001",
        "Product_Category": "Beauty",
        "Product_Price_INR": 8772.58,
        "Discount_Percent": 20.1,
        "Expected_Delivery_Days": 10,
        "Actual_Delivery_Days": 12,
        "Customer_Rating_PreOrder": 4.1,
        "Previous_Returns": 1,
        "Previous_Orders": 18,
        "Payment_Method": "Card",
        "Damaged_Package_Flag": "No",
        "Package_Size": "Large",
        "Promotion_Active": "No"
    },
    {
        "Order_ID": "ECOM00019",
        "Product_Category": "Electronics",
        "Product_Price_INR": 11763.01,
        "Discount_Percent": 8.1,
        "Expected_Delivery_Days": 16,
        "Actual_Delivery_Days": 14,
        "Customer_Rating_PreOrder": 3.0,
        "Previous_Returns": 5,
        "Previous_Orders": 15,
        "Payment_Method": "UPI",
        "Damaged_Package_Flag": "Yes",
        "Package_Size": "Small",
        "Promotion_Active": "No"
    },
    {
        "Order_ID": "ECOM00020",
        "Product_Category": "Home",
        "Product_Price_INR": 20610.60,
        "Discount_Percent": 4.9,
        "Expected_Delivery_Days": 7,
        "Actual_Delivery_Days": 7,
        "Customer_Rating_PreOrder": 2.5,
        "Previous_Returns": 0,
        "Previous_Orders": 18,
        "Payment_Method": "COD",
        "Damaged_Package_Flag": "No",
        "Package_Size": "Medium",
        "Promotion_Active": "Yes"
    }
]


def test_api():
    print("=" * 80)
    print("  TESTING E-COMMERCE PRODUCT RETURN PREDICTION SYSTEM")
    print("=" * 80)

    # 1. Health check
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"[HEALTH CHECK] Status Code: {r.status_code}")
        print("Response:", json.dumps(r.json(), indent=2))
    except Exception as e:
        print(f"[ERROR] Could not connect to {BASE_URL}: {e}")
        return

    print("\n" + "-" * 80)
    print("  TESTING SINGLE INFERENCE: POST /predict")
    print("-" * 80)

    for order in SAMPLE_ORDERS:
        r = requests.post(f"{BASE_URL}/predict", json=order)
        if r.status_code == 200:
            res = r.json()
            print(f"Order: {res['order_id']} | Category: {order['Product_Category']:<11} | "
                  f"Prediction: {res['prediction']:<12} | Prob: {res['return_probability']:.2%} | "
                  f"Risk: {res['risk_level']:<6} | Delay: {res['delivery_delay_days']:+d}d")
        else:
            print(f"Error {r.status_code}: {r.text}")

    print("\n" + "-" * 80)
    print("  TESTING BATCH INFERENCE: POST /predict/batch")
    print("-" * 80)

    batch_payload = {"orders": SAMPLE_ORDERS}
    r = requests.post(f"{BASE_URL}/predict/batch", json=batch_payload)
    if r.status_code == 200:
        data = r.json()
        print(f"Total Processed: {data['total_orders']} | "
              f"Returned: {data['returned_count']} | Not Returned: {data['not_returned_count']}")
    else:
        print(f"Batch Error {r.status_code}: {r.text}")

    print("=" * 80)


if __name__ == "__main__":
    test_api()
