"""
FastAPI Application for E-Commerce Product Return Prediction.

Endpoints:
- GET  /        : API overview and metadata
- GET  /health  : Health check and model readiness status
- POST /predict : Real-time single order product return prediction
- POST /predict/batch : Batch order prediction endpoint
"""

import os
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

import joblib
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.feature_engineering import engineer_features

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("return_prediction_api")

MODEL_PATH = os.path.join("models", "best_model.joblib")
METADATA_PATH = os.path.join("models", "model_metadata.json")

model_pipeline = None
model_metadata = {}


def load_artifacts():
    global model_pipeline, model_metadata
    try:
        if os.path.exists(MODEL_PATH):
            model_pipeline = joblib.load(MODEL_PATH)
            logger.info("Successfully loaded ML model pipeline from: %s", MODEL_PATH)
        else:
            logger.warning("Model file not found at %s. Please run train_model.py first.", MODEL_PATH)

        if os.path.exists(METADATA_PATH):
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                model_metadata = json.load(f)
            logger.info("Loaded model metadata: %s", model_metadata.get("model_name"))
    except Exception as e:
        logger.error("Error loading model artifacts: %s", e)


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_artifacts()
    yield


app = FastAPI(
    title="E-Commerce Product Return Prediction API",
    description=(
        "Production ML inference API predicting whether e-commerce orders "
        "will be Returned or Not Returned based on customer, product, and delivery attributes."
    ),
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic Input Schemas
class OrderInput(BaseModel):
    Order_ID: Optional[str] = Field(default="ECOM_SAMPLE", description="Unique Order Identifier")
    Product_Category: str = Field(..., description="Category: Beauty, Fashion, Electronics, Home, Sports")
    Product_Price_INR: float = Field(..., gt=0, description="Product price in INR (must be > 0)")
    Discount_Percent: float = Field(..., ge=0, le=100, description="Discount percentage applied (0-100)")
    Expected_Delivery_Days: int = Field(..., ge=1, le=30, description="Expected delivery duration in days")
    Actual_Delivery_Days: int = Field(..., ge=1, le=30, description="Actual delivery duration in days")
    Customer_Rating_PreOrder: float = Field(..., ge=1.0, le=5.0, description="Pre-order rating by customer (1.0 to 5.0)")
    Previous_Returns: int = Field(..., ge=0, description="Number of previous returns by this customer")
    Previous_Orders: int = Field(..., ge=1, description="Total previous orders by this customer")
    Payment_Method: str = Field(..., description="Payment method: Card, COD, Wallet, UPI")
    Damaged_Package_Flag: str = Field(..., description="Damaged package reported: 'Yes' or 'No'")
    Package_Size: str = Field(..., description="Package dimensions: 'Small', 'Medium', 'Large'")
    Promotion_Active: str = Field(..., description="Promotion active on product: 'Yes' or 'No'")


class PredictionResponse(BaseModel):
    order_id: str
    prediction: str
    predicted_class: int
    return_probability: float
    risk_level: str
    delivery_delay_days: int
    customer_return_frequency: float
    effective_price_inr: float
    return_reason_summary: str
    model_name: str
    model_version: str
    timestamp: str


class BatchOrderInput(BaseModel):
    orders: List[OrderInput]


class BatchPredictionResponse(BaseModel):
    total_orders: int
    returned_count: int
    not_returned_count: int
    predictions: List[PredictionResponse]


# Endpoints
@app.get("/", tags=["General"])
def root():
    return {
        "service": "E-Commerce Product Return Prediction API",
        "status": "online",
        "version": "1.1.0",
        "student": {
            "name": "Velpuri Bhanu Teja",
            "register_number": "231FA04E85",
            "github_profile": "https://github.com/BhanuTeja33"
        },
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "batch_predict": "/predict/batch",
            "documentation": "/docs"
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    global model_pipeline
    is_ready = model_pipeline is not None
    return {
        "status": "healthy" if is_ready else "degraded",
        "model_loaded": is_ready,
        "model_name": model_metadata.get("model_name", "Logistic_Regression"),
        "model_version": "1.1.0",
        "timestamp": datetime.now().isoformat(),
        "student": "Velpuri Bhanu Teja (231FA04E85)"
    }


def _generate_reason(prob: float, delay: int, freq: float, damaged: str) -> str:
    reasons = []
    if damaged.lower() == "yes":
        reasons.append("Damaged package reported")
    if delay > 0:
        reasons.append(f"Delivery delayed by {delay} day(s)")
    if freq >= 0.25:
        reasons.append(f"High historical return rate ({freq:.1%})")
    if prob >= 0.50 and not reasons:
        reasons.append("Model identified composite risk from product and rating patterns")
    if prob < 0.50:
        reasons.append("Order parameters indicate low return risk")
    return "; ".join(reasons)


def _process_prediction(item: OrderInput) -> PredictionResponse:
    global model_pipeline

    if model_pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Train the model first."
        )

    # 1. Convert input to DataFrame
    raw_dict = item.model_dump()
    df_single = pd.DataFrame([raw_dict])

    # 2. Run Feature Engineering
    engineered_df = engineer_features(df_single)

    # 3. Model Inference
    pred_int = int(model_pipeline.predict(engineered_df)[0])
    prob_float = float(model_pipeline.predict_proba(engineered_df)[0][1])

    # Determine risk category
    if prob_float >= 0.65:
        risk = "High"
    elif prob_float >= 0.40:
        risk = "Medium"
    else:
        risk = "Low"

    prediction_label = "Returned" if pred_int == 1 else "Not Returned"

    delay = int(engineered_df["delivery_delay"].iloc[0])
    freq = round(float(engineered_df["customer_return_frequency"].iloc[0]), 4)
    eff_price = round(float(engineered_df["effective_price"].iloc[0]), 2)
    reason = _generate_reason(prob_float, delay, freq, item.Damaged_Package_Flag)

    return PredictionResponse(
        order_id=item.Order_ID or "N/A",
        prediction=prediction_label,
        predicted_class=pred_int,
        return_probability=round(prob_float, 4),
        risk_level=risk,
        delivery_delay_days=delay,
        customer_return_frequency=freq,
        effective_price_inr=eff_price,
        return_reason_summary=reason,
        model_name=model_metadata.get("model_name", "Logistic_Regression"),
        model_version="1.1.0",
        timestamp=datetime.now().isoformat()
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Inference"])
def predict_return(order: OrderInput):
    """
    Predict whether a single e-commerce product order is likely to be returned.
    """
    try:
        return _process_prediction(order)
    except Exception as e:
        logger.error("Prediction error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["Inference"])
def predict_batch(batch: BatchOrderInput):
    """
    Batch prediction endpoint for multiple orders.
    """
    try:
        results = [_process_prediction(order) for order in batch.orders]
        returned = sum(1 for r in results if r.prediction == "Returned")
        not_returned = len(results) - returned
        return BatchPredictionResponse(
            total_orders=len(results),
            returned_count=returned,
            not_returned_count=not_returned,
            predictions=results
        )
    except Exception as e:
        logger.error("Batch prediction error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
