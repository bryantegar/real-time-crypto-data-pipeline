import json
from kafka import KafkaConsumer

print("📊 Live Monitor started... listening Kafka stream")

consumer = KafkaConsumer(
    "crypto_prices",
    bootstrap_servers="localhost:9092",
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),
    auto_offset_reset='latest'
)

for msg in consumer:
    data = msg.value
    price = data["price"]
    symbol = data["symbol"]
    ts = data["timestamp"]

    print(f"🔹 {symbol} | 💵 {price} | 🕒 {ts}")