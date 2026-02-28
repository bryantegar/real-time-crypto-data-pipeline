import asyncio
import json
import os
from datetime import datetime

import psycopg2
import websockets

# ====== PostgreSQL CONFIG (sesuaikan dengan docker-compose) ======
PG_HOST = "localhost"
PG_PORT = 5432
PG_DB = "crypto_db"
PG_USER = "crypto_user"
PG_PASS = "crypto_pass"

# ====== QUERY DASAR ======
SQL_LATEST_PRICE = """
SELECT symbol, price, EXTRACT(EPOCH FROM ts) AS ts
FROM crypto_realtime_prices
ORDER BY id DESC
LIMIT 1;
"""

SQL_LATEST_OHLC = """
SELECT symbol, open, high, low, close, end_ts
FROM crypto_agg_5min
ORDER BY id DESC
LIMIT 1;
"""

# ====== KONEKSI POSTGRES ======
def get_pg_conn():
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASS,
    )


async def send_updates(websocket):
    """Loop kirim update price + OHLC ke satu client."""
    print("🟢 Client connected to WebSocket")

    # koneksi DB khusus untuk client ini
    conn = get_pg_conn()
    cur = conn.cursor()

    try:
        while True:
            # --- latest price ---
            cur.execute(SQL_LATEST_PRICE)
            row = cur.fetchone()
            if row:
                symbol, price, ts_epoch = row
                msg_price = {
                    "type": "price",
                    "symbol": symbol,
                    "price": float(price),
                    "timestamp": float(ts_epoch),
                }
                await websocket.send(json.dumps(msg_price))
                print(f"📤 Sent price: {symbol} {price}")

            # --- latest OHLC 5 min ---
            cur.execute(SQL_LATEST_OHLC)
            row = cur.fetchone()
            if row:
                symbol, o, h, l, c, interval_end = row
                msg_ohlc = {
                    "type": "ohlc",
                    "symbol": symbol,
                    "open": float(o),
                    "high": float(h),
                    "low": float(l),
                    "close": float(c),
                    "interval_end": end_ts.isoformat(),
                }
                await websocket.send(json.dumps(msg_ohlc))
                print(f"📤 Sent OHLC: {symbol} {interval_end} O:{o} H:{h} L:{l} C:{c}")

            # tunggu 2 detik sebelum polling lagi
            await asyncio.sleep(2)

    except websockets.exceptions.ConnectionClosed:
        print("🔌 Client disconnected")
    finally:
        cur.close()
        conn.close()


async def ws_main():
    async with websockets.serve(send_updates, "localhost", 8765):
        print("🔌 WebSocket server running at ws://localhost:8765")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(ws_main())
