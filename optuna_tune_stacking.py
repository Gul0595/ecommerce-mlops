import optuna
import pickle
import mysql.connector
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import GradientBoostingRegressor, StackingRegressor
from sklearn.linear_model import LinearRegression, Lasso, Ridge


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
FINAL_MODEL_PATH = f"{MODEL_DIR}/StackingEnsemble_Optuna.pkl"


# =========================
# Load dataset
# =========================
def load_data():
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

    return train_test_split(X, y, test_size=0.2, random_state=42)


# =========================
# Optuna Objective
# =========================
def objective(trial):

    gb_params = {
        "n_estimators": trial.suggest_int("gb_n_estimators", 50, 300),
        "learning_rate": trial.suggest_float("gb_lr", 0.01, 0.2),
        "max_depth": trial.suggest_int("gb_max_depth", 2, 6),
        "subsample": trial.suggest_float("gb_subsample", 0.7, 1.0),
        "random_state": 42,
    }

    ridge_alpha = trial.suggest_float("ridge_alpha", 0.1, 10.0, log=True)

    base_models = [
        ("gb", GradientBoostingRegressor(**gb_params)),
        ("lr", LinearRegression()),
        ("lasso", Lasso(alpha=0.01)),
    ]

    meta_model = Ridge(alpha=ridge_alpha)

    stacking = StackingRegressor(
        estimators=base_models,
        final_estimator=meta_model,
        n_jobs=-1,
    )

    X_train, X_test, y_train, y_test = load_data()

    stacking.fit(X_train, y_train)
    preds = stacking.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, preds))
    return rmse


# =========================
# Run Optuna
# =========================
def run_optuna():

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=30, timeout=600)

    print("\n🏆 Best RMSE:", study.best_value)
    print("🔧 Best Parameters:")
    for k, v in study.best_params.items():
        print(f"  {k}: {v}")

    # ---- Retrain final model on full data ----
    gb_best = GradientBoostingRegressor(
        n_estimators=study.best_params["gb_n_estimators"],
        learning_rate=study.best_params["gb_lr"],
        max_depth=study.best_params["gb_max_depth"],
        subsample=study.best_params["gb_subsample"],
        random_state=42,
    )

    ridge_best = Ridge(
        alpha=study.best_params["ridge_alpha"]
    )

    final_model = StackingRegressor(
        estimators=[
            ("gb", gb_best),
            ("lr", LinearRegression()),
            ("lasso", Lasso(alpha=0.01)),
        ],
        final_estimator=ridge_best,
        n_jobs=-1,
    )

    # Load full dataset
    db = mysql.connector.connect(**DB_CONFIG)
    df = pd.read_sql(
        """
        SELECT
            total_orders,
            total_quantity,
            avg_price,
            avg_discount_pct,
            city_count,
            total_revenue
        FROM daily_product_features
        """,
        db,
    )
    db.close()

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

    final_model.fit(X, y)

    with open(FINAL_MODEL_PATH, "wb") as f:
        pickle.dump(final_model, f)

    print(f"\n✅ Final Optuna-tuned stacking model saved → {FINAL_MODEL_PATH}")


# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    run_optuna()
