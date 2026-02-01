import mysql.connector
import pandas as pd

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "root",
    "password": "",
    "database": "ecommerce_db",
}

def build_daily_product_features():
    db = mysql.connector.connect(**DB_CONFIG)

    query = """
    SELECT
        DATE(event_time) AS feature_date,
        product_id,
        product_name,
        category,

        COUNT(DISTINCT order_id) AS total_orders,
        SUM(quantity) AS total_quantity,
        SUM(net_amount) AS total_revenue,
        AVG(price) AS avg_price,
        AVG(discount_pct) AS avg_discount_pct,
        COUNT(DISTINCT city) AS city_count

    FROM sales_events
    GROUP BY feature_date, product_id, product_name, category
    """

    df = pd.read_sql(query, db)

    cursor = db.cursor()

    insert_query = """
    INSERT INTO daily_product_features (
        feature_date,
        product_id,
        product_name,
        category,
        total_orders,
        total_quantity,
        total_revenue,
        avg_price,
        avg_discount_pct,
        city_count
    )
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
        total_orders = VALUES(total_orders),
        total_quantity = VALUES(total_quantity),
        total_revenue = VALUES(total_revenue),
        avg_price = VALUES(avg_price),
        avg_discount_pct = VALUES(avg_discount_pct),
        city_count = VALUES(city_count)
    """

    for _, row in df.iterrows():
        cursor.execute(insert_query, tuple(row))

    db.commit()
    cursor.close()
    db.close()

    print(f"Built {len(df)} daily product feature rows")

if __name__ == "__main__":
    build_daily_product_features()
