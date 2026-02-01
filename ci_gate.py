import sys
import mysql.connector
import pandas as pd


DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "root",
    "password": "",
    "database": "ecommerce_db",
}

ALLOWED_DEGRADATION = 1.05  # 5%


def run_ci_gate():
    db = mysql.connector.connect(**DB_CONFIG)

    query = """
        SELECT
            run_time,
            model_name,
            rmse,
            r2,
            data_rows,
            feature_days
        FROM model_benchmarks
        ORDER BY run_time DESC
    """

    df = pd.read_sql(query, db)
    db.close()

    if df.empty:
        print("⚠️ No benchmark data found. PASS by default.")
        return 0

    # ---- Identify distinct runs ----
    run_times = df["run_time"].drop_duplicates().sort_values(ascending=False)

    if len(run_times) < 2:
        print("⚠️ Only one benchmark run found. PASS by default.")
        return 0

    latest_time = run_times.iloc[0]
    prev_time = run_times.iloc[1]

    latest = df[df["run_time"] == latest_time]
    previous = df[df["run_time"] == prev_time]

    latest_best = latest.sort_values("rmse").iloc[0]
    previous_best = previous.sort_values("rmse").iloc[0]

    print("\n🔍 CI Gate Evaluation")
    print("---------------------")
    print(f"Latest best model   : {latest_best['model_name']}")
    print(f"Latest RMSE         : {latest_best['rmse']}")
    print(f"Previous best RMSE  : {previous_best['rmse']}")
    print(f"Latest R²           : {latest_best['r2']}")
    print(f"Data rows           : {latest_best['data_rows']}")
    print(f"Feature days        : {latest_best['feature_days']}")

    # ---- HARD FAIL CONDITIONS ----
    if latest_best["data_rows"] < 20:
        print("❌ CI FAIL: Not enough data rows")
        return 1

    if latest_best["r2"] < 0.85:
        print("❌ CI FAIL: R² below acceptable threshold")
        return 1

    # ---- PERFORMANCE REGRESSION CHECK ----
    if latest_best["rmse"] > previous_best["rmse"] * ALLOWED_DEGRADATION:
        print("❌ CI FAIL: RMSE regression beyond allowed threshold")
        return 1

    print("✅ CI PASS: Model performance acceptable")
    return 0


if __name__ == "__main__":
    sys.exit(run_ci_gate())





















