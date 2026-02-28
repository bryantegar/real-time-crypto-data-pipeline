import json
import time
import psycopg2
from kafka import KafkaConsumer

# 🎯 Kafka Config
consumer = KafkaConsumer(
    "crypto_prices",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

# 🗄 Database Config
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="crypto_db",
    user="crypto_user",
    password="crypto_pass"
)
cur = conn.cursor()

print("📥 Consumer PG → DB Started...")

SQL_INSERT = """
INSERT INTO crypto_realtime_prices(symbol, price, ts)
VALUES (%s, %s, to_timestamp(%s))
"""

try:
    for msg in consumer:
        data = msg.value

        symbol = data.get("symbol")
        price = data.get("price")
        ts_epoch = data.get("timestamp")

        if price == 0 or price is None:
            print("⚠ Skip, invalid price:", data)
            continue

        cur.execute(SQL_INSERT, (symbol, price, ts_epoch))
        conn.commit()

        print(f"💾 Insert to DB: {symbol} {price}")

except KeyboardInterrupt:
    print("\n⛔ Consumer stopped")

finally:
    cur.close()
    conn.close()
