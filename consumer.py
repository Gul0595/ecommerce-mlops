import json
from kafka import KafkaConsumer
import mysql.connector
from datetime import datetime

# Kafka Consumer
consumer = KafkaConsumer(
    "ecommerce_sales",
    bootstrap_servers="127.0.0.1:9092",
    api_version=(3, 7, 0),
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

# MySQL connection
db = mysql.connector.connect(
    host="127.0.0.1",
    port=3307, 
    user="root",
    password="",  
    database="ecommerce_db"
)

cursor = db.cursor()

insert_query = """
INSERT INTO sales_events (
    order_id, user_id, customer_type,
    product_id, product_name, category, brand,
    city, region,
    price, quantity, discount_pct, discount_amount,
    gross_amount, net_amount,
    payment_method,
    event_time, order_date, order_hour, order_day
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

print("Kafka Consumer → MySQL started...")

for message in consumer:
    data = message.value

    # Insert into MySQL
    cursor.execute(
        insert_query,
        (
            data["order_id"],
            data["user_id"],
            data["customer_type"],

            data["product_id"],
            data["product_name"],
            data["category"],
            data["brand"],

            data["city"],
            data["region"],

            data["price"],
            data["quantity"],
            data["discount_pct"],
            data["discount_amount"],
            data["gross_amount"],
            data["net_amount"],

            data["payment_method"],

            datetime.fromisoformat(data["event_time"]),
            data["order_date"],
            data["order_hour"],
            data["order_day"]
        )
    )

    db.commit()

    # Your existing log (unchanged in spirit)
    print(
        f"Consumed | {data['event_time']} | "
        f"{data['order_id']} | "
        f"{data['product_name']} | "
        f"{data['category']} | "
        f"{data['city']} | "
        f"Qty:{data['quantity']} | "
        f"Discount:{data['discount_pct']}% "
        f"(₹{data['discount_amount']}) | "
        f"Net: ₹{data['net_amount']}"
    )
