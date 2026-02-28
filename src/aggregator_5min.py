import os
import time
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = os.getenv("PG_PORT", "5432")
PG_DB   = os.getenv("PG_DB", "crypto_db")
PG_USER = os.getenv("PG_USER", "crypto_user")
PG_PASS = os.getenv("PG_PASS", "crypto_pass")


def get_conn():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASS
    )


def aggregate_5min():
    conn = get_conn()
    cursor = conn.cursor()

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=5)

    query = """
    SELECT symbol, price, ts
    FROM crypto_realtime_prices
    WHERE ts BETWEEN %s AND %s
    ORDER BY ts ASC
    """

    df = pd.read_sql(query, conn, params=(start_time, end_time))

    if df.empty:
        print("⚠ No data found in last 5 minutes")
        conn.close()
        return

    grouped = df.groupby("symbol").agg(
        open=("price", "first"),
        high=("price", "max"),
        low=("price", "min"),
        close=("price", "last"),
    ).reset_index()

    for _, row in grouped.iterrows():
        cursor.execute("""
            INSERT INTO crypto_ohlc_5min(symbol, open, high, low, close, start_ts, end_ts)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (row["symbol"], row["open"], row["high"], row["low"], row["close"], start_time, end_time))

        print(f"📦 Aggregated → {row['symbol']} | OHLC: {row['open']}/{row['high']}/{row['low']}/{row['close']}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    print("⏱ OHLC Aggregator 5-Minute Started!")

    while True:
        try:
            aggregate_5min()
        except Exception as e:
            print("❌ Aggregation Error:", e)

        print("😴 Sleep for 5 minutes...\n")
        time.sleep(30)
