import os
import pickle
import mysql.connector
import pandas as pd

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor


# =========================
# Configuration
# =========================
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "root",
    "password": "",
    "database": "ecommerce_db",
}

MODEL_DIR = "models"
TOP_K = 3


# =========================
# Model registry
# =========================
MODEL_REGISTRY = {
    "LinearRegression": LinearRegression(),
    "Ridge": Ridge(alpha=1.0),
    "Lasso": Lasso(alpha=0.01),
    "RandomForest": RandomForestRegressor(
        n_estimators=100, random_state=42
    ),
    "GradientBoosting": GradientBoostingRegressor(
        random_state=42
    ),
}


# =========================
# Train Top Models
# =========================
def train_top_models():

    os.makedirs(MODEL_DIR, exist_ok=True)

    db = mysql.connector.connect(**DB_CONFIG)

    # --- Get latest benchmark run ---
    bench_query = """
        SELECT *
        FROM model_benchmarks
        WHERE run_time = (
            SELECT MAX(run_time) FROM model_benchmarks
        )
        ORDER BY rmse ASC
        LIMIT %s
    """

    benchmark_df = pd.read_sql(
        bench_query, db, params=(TOP_K,)
    )

    if benchmark_df.empty:
        raise ValueError("No benchmark data found")

    top_models = benchmark_df["model_name"].tolist()

    print("\n🏆 Top models selected:")
    for i, m in enumerate(top_models, 1):
        print(f"{i}. {m}")

    # --- Load full feature data ---
    feature_query = """
        SELECT
            total_orders,
            total_quantity,
            avg_price,
            avg_discount_pct,
            city_count,
            total_revenue
        FROM daily_product_features
    """

    df = pd.read_sql(feature_query, db)
    db.close()

    if df.empty:
        raise ValueError("No feature data found")

    X = df[
        [
            "total_orders",
            "total_quantity",
            "avg_price",
            "avg_discount_pct",
            "city_count",
        ]
    ]
    y = df["total_revenue"]

    trained_models = {}

    # --- Train each model ---
    for model_name in top_models:
        print(f"\n🔁 Training {model_name} on full dataset...")

        model = MODEL_REGISTRY[model_name]
        model.fit(X, y)

        model_path = os.path.join(
            MODEL_DIR, f"{model_name}.pkl"
        )

        with open(model_path, "wb") as f:
            pickle.dump(model, f)

        trained_models[model_name] = model_path

        print(f"✅ Saved model → {model_path}")

    print("\n🎉 Top models trained and saved successfully")

    return trained_models


# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    train_top_models()
