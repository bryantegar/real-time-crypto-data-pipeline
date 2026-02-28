import json
import time
from datetime import datetime, timezone
from kafka import KafkaConsumer
import psycopg2

# Kafka config
KAFKA_TOPIC = "crypto_prices"
KAFKA_SERVER = "localhost:9092"

# PostgreSQL config
DB_CONFIG = {
    "dbname": "crypto_db",
    "user": "crypto_user",
    "password": "crypto_pass",
    "host": "localhost",
    "port": 5432
}

def connect_db():
    """Connect to PostgreSQL database"""
    while True:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cur = conn.cursor()
            print("🔗 Connected to PostgreSQL")
            return conn, cur
        except Exception as e:
            print(f"❌ DB Connect Error: {e}, retrying in 5 sec...")
            time.sleep(5)


def main():
    print("💾 DB Consumer started — waiting data from Kafka...")

    # Kafka consumer
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        auto_offset_reset="latest",
        enable_auto_commit=True
    )

    conn, cur = connect_db()

    for msg in consumer:
        data = msg.value

        try:
            symbol = data.get("symbol", "BTCUSDT")
            price = float(data.get("price", 0.0))

            # ✔ Timestamp now in UTC format (timezone-aware)
            ts = datetime.now(timezone.utc)

            cur.execute(
                """
                INSERT INTO crypto_realtime_prices(symbol, price, ts)
                VALUES (%s, %s, %s)
                """,
                (symbol, price, ts)
            )
            conn.commit()

            print(f"🆕 INSERTED ➜ {symbol} | {price} | {ts}")

        except Exception as e:
            print(f"❌ Insert Error: {e}")
            conn.rollback()
            conn, cur = connect_db()  # Auto reconnect DB


if __name__ == "__main__":
    main()
