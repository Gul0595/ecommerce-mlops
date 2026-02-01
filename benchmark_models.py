import time
import mysql.connector
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor


# =========================
# Database Configuration
# =========================
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "root",
    "password": "",
    "database": "ecommerce_db",
}


# =========================
# Benchmark Runner
# =========================
def run_benchmark():

    # --- Load feature data ---
    db = mysql.connector.connect(**DB_CONFIG)

    query = """
        SELECT
            feature_date,
            product_id,
            total_orders,
            total_quantity,
            total_revenue,
            avg_price,
            avg_discount_pct,
            city_count
        FROM daily_product_features
        ORDER BY feature_date
    """

    df = pd.read_sql(query, db)
    db.close()

    # --- Safety guard ---
    if df.empty or len(df) < 20:
        raise ValueError("Not enough data to benchmark models yet")

    data_rows = len(df)
    feature_days = df["feature_date"].nunique()

    # --- Feature matrix & target ---
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

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # --- Models ---
    models = {
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

    results = []

    # --- Train & evaluate ---
    for name, model in models.items():
        start = time.time()

        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        train_time = round(time.time() - start, 2)

        mse = mean_squared_error(y_test, preds)
        rmse = round(np.sqrt(mse), 3)
        mae = round(mean_absolute_error(y_test, preds), 3)
        r2 = round(r2_score(y_test, preds), 3)

        results.append(
            {
                "model": name,
                "rmse": rmse,
                "mae": mae,
                "r2": r2,
                "train_time_sec": train_time,
            }
        )

    # --- Leaderboard ---
    results_df = pd.DataFrame(results).sort_values("rmse")

    print("\n📊 Model Benchmark Results (lower RMSE is better):")
    print(results_df.to_string(index=False))

    # =========================
    # Save to MySQL
    # =========================
    db_out = mysql.connector.connect(**DB_CONFIG)
    cursor = db_out.cursor()

    insert_query = """
        INSERT INTO model_benchmarks (
            model_name,
            rmse,
            mae,
            r2,
            train_time_sec,
            data_rows,
            feature_days
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    for _, row in results_df.iterrows():
        cursor.execute(
            insert_query,
            (
                row["model"],
                row["rmse"],
                row["mae"],
                row["r2"],
                row["train_time_sec"],
                data_rows,
                feature_days,
            )
        )

    db_out.commit()
    cursor.close()
    db_out.close()

    print("\n✅ Benchmark results saved to MySQL")


# =========================
# Entry Point
# =========================
if __name__ == "__main__":
    run_benchmark()
