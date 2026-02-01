import os
import pickle
import mysql.connector
import pandas as pd

from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import GradientBoostingRegressor


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
STACKING_PATH = os.path.join(MODEL_DIR, "StackingEnsemble.pkl")


# =========================
# Train Stacking Model
# =========================
def train_stacking():

    print("\n🧠 Training Stacking Regressor...")

    # Base models (fresh instances)
    base_estimators = [
        ("gb", GradientBoostingRegressor(random_state=42)),
        ("lr", LinearRegression()),
        ("lasso", Lasso(alpha=0.01)),
    ]

    meta_model = Ridge(alpha=1.0)

    stacking_model = StackingRegressor(
        estimators=base_estimators,
        final_estimator=meta_model,
        passthrough=False,   # important for stability
        n_jobs=-1
    )

    # ---- Load full dataset ----
    db = mysql.connector.connect(**DB_CONFIG)

    query = """
        SELECT
            total_orders,
            total_quantity,
            avg_price,
            avg_discount_pct,
            city_count,
            total_revenue
        FROM daily_product_features
    """

    df = pd.read_sql(query, db)
    db.close()

    if df.empty:
        raise ValueError("No data found for stacking model")

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

    stacking_model.fit(X, y)

    with open(STACKING_PATH, "wb") as f:
        pickle.dump(stacking_model, f)

    print(f"✅ Stacking Ensemble saved → {STACKING_PATH}")
    print("🎉 Stacking model ready")


# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    train_stacking()
