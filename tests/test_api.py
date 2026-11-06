"""
Integration Tests for FastAPI Prediction Endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from app import app, load_artifacts


@pytest.fixture(scope="module", autouse=True)
def setup_api():
    """Ensure artifacts are loaded before running API tests."""
    load_artifacts()


client = TestClient(app)


def test_root_endpoint():
    """Test GET / returns 200 and student metadata."""
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "online"
    assert "student" in data
    assert data["student"]["register_number"] == "231FA04E85"


def test_health_endpoint():
    """Test GET /health returns 200 and healthy status."""
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_predict_single_endpoint_valid():
    """Test POST /predict with a realistic payload."""
    payload = {
        "Order_ID": "ECOM_TEST_001",
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
    }
    res = client.post("/predict", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "prediction" in data
    assert data["prediction"] in ["Returned", "Not Returned"]
    assert 0.0 <= data["return_probability"] <= 1.0
    assert data["risk_level"] in ["High", "Medium", "Low"]
    assert data["delivery_delay_days"] == 3


def test_predict_single_endpoint_invalid_price():
    """Test POST /predict with invalid price (<= 0) triggers validation error."""
    payload = {
        "Order_ID": "ECOM_BAD_PRICE",
        "Product_Category": "Electronics",
        "Product_Price_INR": -100.0,
        "Discount_Percent": 10.0,
        "Expected_Delivery_Days": 5,
        "Actual_Delivery_Days": 6,
        "Customer_Rating_PreOrder": 4.0,
        "Previous_Returns": 0,
        "Previous_Orders": 5,
        "Payment_Method": "Card",
        "Damaged_Package_Flag": "No",
        "Package_Size": "Small",
        "Promotion_Active": "No"
    }
    res = client.post("/predict", json=payload)
    assert res.status_code == 422


def test_batch_prediction_endpoint():
    """Test POST /predict/batch with multiple orders."""
    payload = {
        "orders": [
            {
                "Order_ID": "ECOM_BATCH_1",
                "Product_Category": "Beauty",
                "Product_Price_INR": 8772.58,
                "Discount_Percent": 20.1,
                "Expected_Delivery_Days": 10,
                "Actual_Delivery_Days": 12,
                "Customer_Rating_PreOrder": 4.1,
                "Previous_Returns": 3,
                "Previous_Orders": 18,
                "Payment_Method": "Card",
                "Damaged_Package_Flag": "No",
                "Package_Size": "Large",
                "Promotion_Active": "No"
            },
            {
                "Order_ID": "ECOM_BATCH_2",
                "Product_Category": "Fashion",
                "Product_Price_INR": 14000.0,
                "Discount_Percent": 15.0,
                "Expected_Delivery_Days": 4,
                "Actual_Delivery_Days": 7,
                "Customer_Rating_PreOrder": 2.5,
                "Previous_Returns": 6,
                "Previous_Orders": 10,
                "Payment_Method": "COD",
                "Damaged_Package_Flag": "Yes",
                "Package_Size": "Medium",
                "Promotion_Active": "Yes"
            }
        ]
    }
    res = client.post("/predict/batch", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["total_orders"] == 2
    assert len(data["predictions"]) == 2
