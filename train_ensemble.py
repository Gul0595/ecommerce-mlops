import os
import pickle
import mysql.connector
import pandas as pd

from sklearn.ensemble import VotingRegressor


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
ENSEMBLE_PATH = os.path.join(MODEL_DIR, "VotingEnsemble.pkl")


# =========================
# Load trained models
# =========================
def load_model(name):
    path = os.path.join(MODEL_DIR, f"{name}.pkl")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found: {path}")

    with open(path, "rb") as f:
        return pickle.load(f)


# =========================
# Train Voting Ensemble
# =========================
def train_voting_ensemble():

    print("\n🤝 Building Voting Ensemble...")

    gb = load_model("GradientBoosting")
    lr = load_model("LinearRegression")
    lasso = load_model("Lasso")

    ensemble = VotingRegressor(
        estimators=[
            ("gb", gb),
            ("lr", lr),
            ("lasso", lasso),
        ]
    )

    # --- Load full feature data ---
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
        raise ValueError("No feature data found for ensemble training")

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

    ensemble.fit(X, y)

    with open(ENSEMBLE_PATH, "wb") as f:
        pickle.dump(ensemble, f)

    print(f"✅ Voting Ensemble saved → {ENSEMBLE_PATH}")
    print("🎉 Ensemble model ready for deployment")


# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    train_voting_ensemble()
