import json
import time
from kafka import KafkaProducer
from data_generator.generator import generate_order

producer = KafkaProducer(
    bootstrap_servers="127.0.0.1:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

TOPIC = "ecommerce_sales"

print("Kafka Producer started...")

while True:
    order = generate_order()
    producer.send(TOPIC, value=order)

    print(
        f"Produced | {order['event_time']} | "
        f"{order['order_id']} | "
        f"{order['product_name']} | "
        f"{order['category']} | "
        f"{order['city']} | "
        f"Qty:{order['quantity']} | "
        f"Discount:{order['discount_pct']}% "
        f"(₹{order['discount_amount']}) | "
        f"Net: ₹{order['net_amount']}"
)

    time.sleep(1)
