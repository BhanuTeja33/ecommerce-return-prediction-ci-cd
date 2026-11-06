"""
Model Training and Evaluation Pipeline.

Trains at least two classification models:
1. Logistic Regression (Linear baseline with class balancing)
2. Random Forest Classifier (Non-linear ensemble with class balancing)
3. Gradient Boosting Classifier (Boosting comparative model)

Evaluates performance using Accuracy, Precision, Recall, F1-Score, and ROC-AUC.
Saves the best-performing pipeline and evaluation reports.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Tuple

import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from src.data_preprocessing import handle_missing_values
from src.feature_engineering import engineer_features

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("model_trainer")


# Feature schema definition
CATEGORICAL_FEATURES = [
    "Product_Category",
    "Payment_Method",
    "Damaged_Package_Flag",
    "Package_Size",
    "Promotion_Active",
]

NUMERICAL_FEATURES = [
    "Product_Price_INR",
    "Discount_Percent",
    "Expected_Delivery_Days",
    "Actual_Delivery_Days",
    "Customer_Rating_PreOrder",
    "Previous_Returns",
    "Previous_Orders",
    "delivery_delay",
    "customer_return_frequency",
    "effective_price",
    "is_delayed",
    "return_risk_score",
]

ALL_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES


def build_preprocessor() -> ColumnTransformer:
    """
    Constructs the ColumnTransformer pipeline for feature scaling and encoding.
    """
    num_transformer = Pipeline(steps=[
        ("scaler", StandardScaler())
    ])

    cat_transformer = Pipeline(steps=[
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_transformer, NUMERICAL_FEATURES),
            ("cat", cat_transformer, CATEGORICAL_FEATURES),
        ]
    )
    return preprocessor


def evaluate_model(
    pipeline: Pipeline,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    model_name: str
) -> Dict[str, Any]:
    """
    Computes comprehensive classification metrics.
    """
    y_pred = pipeline.predict(X_test)
    y_prob = pipeline.predict_proba(X_test)[:, 1] if hasattr(pipeline, "predict_proba") else y_pred

    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, zero_division=0))
    rec = float(recall_score(y_test, y_pred, zero_division=0))
    f1 = float(f1_score(y_test, y_pred, zero_division=0))
    roc_auc = float(roc_auc_score(y_test, y_prob))
    cm = confusion_matrix(y_test, y_pred).tolist()

    report = {
        "model_name": model_name,
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "roc_auc": round(roc_auc, 4),
        "confusion_matrix": cm,
        "classification_report": classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    }
    return report


def train_models(
    data_path: str = "data/ecommerce_returns.csv",
    models_dir: str = "models",
    reports_dir: str = "reports"
) -> Tuple[Pipeline, Dict[str, Any]]:
    """
    Executes end-to-end model training, comparative evaluation, and artifact saving.
    """
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    # 1. Load dataset
    if not os.path.exists(data_path):
        if os.path.exists("ecommerce_returns.csv"):
            data_path = "ecommerce_returns.csv"
        else:
            raise FileNotFoundError(f"Dataset not found at {data_path}")

    logger.info("Loading e-commerce dataset from: %s", data_path)
    raw_df = pd.read_csv(data_path, encoding="utf-8-sig")
    logger.info("Loaded dataset shape: %s", raw_df.shape)

    # 2. Preprocess & Feature Engineering
    cleaned_df, imputer_stats = handle_missing_values(raw_df)
    engineered_df = engineer_features(cleaned_df)

    # 3. Target Encoding
    target_col = "Return_Status"
    if target_col not in engineered_df.columns:
        raise ValueError(f"Target column '{target_col}' missing from data")

    y = (engineered_df[target_col].str.strip() == "Returned").astype(int)
    X = engineered_df[ALL_FEATURES]

    # Save reference data
    os.makedirs("data", exist_ok=True)
    engineered_df.to_csv("data/reference_data.csv", index=False)

    # 4. Train-Test Split (80/20 Stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    logger.info("Train set: %d samples, Test set: %d samples", len(X_train), len(X_test))

    # 5. Define candidate models
    candidate_models = {
        "Logistic_Regression": LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=42
        ),
        "Random_Forest": RandomForestClassifier(
            n_estimators=120,
            max_depth=8,
            class_weight="balanced",
            random_state=42
        ),
        "Gradient_Boosting": GradientBoostingClassifier(
            n_estimators=100,
            max_depth=4,
            learning_rate=0.08,
            random_state=42
        )
    }

    all_metrics: Dict[str, Any] = {}
    trained_pipelines: Dict[str, Pipeline] = {}

    for name, model in candidate_models.items():
        logger.info("Training candidate model: %s ...", name)
        preprocessor = build_preprocessor()
        pipeline = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", model)
        ])

        pipeline.fit(X_train, y_train)
        metrics = evaluate_model(pipeline, X_test, y_test, name)
        all_metrics[name] = metrics
        trained_pipelines[name] = pipeline

        logger.info(
            "[%s] Accuracy: %.4f | F1: %.4f | Recall: %.4f | ROC AUC: %.4f",
            name, metrics["accuracy"], metrics["f1_score"], metrics["recall"], metrics["roc_auc"]
        )

    # 6. Select best performing model based on balanced F1-Score & ROC AUC
    # Logistic Regression provides best balanced recall/F1 on minority return class
    best_model_name = max(
        all_metrics.keys(),
        key=lambda k: all_metrics[k]["f1_score"] + all_metrics[k]["roc_auc"]
    )
    best_pipeline = trained_pipelines[best_model_name]
    best_metrics = all_metrics[best_model_name]

    logger.info("Selected Best Model: %s", best_model_name)

    # 7. Save model artifact
    best_model_path = os.path.join(models_dir, "best_model.joblib")
    joblib.dump(best_pipeline, best_model_path)
    logger.info("Saved serialized model to: %s", best_model_path)

    # 8. Save metadata
    metadata = {
        "model_name": best_model_name,
        "version": "1.0.0",
        "trained_at": datetime.now().isoformat(),
        "student_name": "Velpuri Bhanu Teja",
        "student_reg_number": "231FA04E85",
        "dataset_rows": len(raw_df),
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "imputer_stats": imputer_stats,
        "features": ALL_FEATURES,
        "performance": best_metrics
    }
    with open(os.path.join(models_dir, "model_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    # 9. Save top-level metrics.json for CI quality gate
    metrics_summary = {
        "best_model": best_model_name,
        "accuracy": best_metrics["accuracy"],
        "f1_score": best_metrics["f1_score"],
        "recall": best_metrics["recall"],
        "precision": best_metrics["precision"],
        "roc_auc": best_metrics["roc_auc"],
        "models_evaluated": list(all_metrics.keys())
    }
    with open("metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics_summary, f, indent=2)

    # 10. Save comprehensive evaluation report
    report_json_path = os.path.join(reports_dir, "model_evaluation_report.json")
    with open(report_json_path, "w", encoding="utf-8") as f:
        json.dump(all_metrics, f, indent=2)

    report_txt_path = os.path.join(reports_dir, "evaluation_metrics.txt")
    with open(report_txt_path, "w", encoding="utf-8") as f:
        f.write("=" * 65 + "\n")
        f.write("  E-COMMERCE PRODUCT RETURN PREDICTION - MODEL EVALUATION REPORT\n")
        f.write("=" * 65 + "\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Student: Velpuri Bhanu Teja | Reg No: 231FA04E85\n\n")
        for m_name, m_data in all_metrics.items():
            f.write(f"--- {m_name} ---\n")
            f.write(f"  Accuracy  : {m_data['accuracy']:.4f}\n")
            f.write(f"  Precision : {m_data['precision']:.4f}\n")
            f.write(f"  Recall    : {m_data['recall']:.4f}\n")
            f.write(f"  F1-Score  : {m_data['f1_score']:.4f}\n")
            f.write(f"  ROC-AUC   : {m_data['roc_auc']:.4f}\n")
            f.write(f"  Confusion Matrix: {m_data['confusion_matrix']}\n\n")
        f.write(f"WINNING MODEL: {best_model_name}\n")
        f.write("=" * 65 + "\n")

    logger.info("Training and evaluation completed successfully!")
    return best_pipeline, all_metrics


if __name__ == "__main__":
    train_models()
