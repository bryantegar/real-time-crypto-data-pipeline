import json
import time
import ssl
from kafka import KafkaProducer
import websocket

# ===== Kafka config =====
KAFKA_BOOTSTRAP = "localhost:9092"
TOPIC = "crypto_prices"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# ===== Binance WebSocket config =====
STREAMS = [
    "btcusdt@trade",
    "ethusdt@trade",
    "bnbusdt@trade",
]

WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@trade"


def on_message(ws, message: str):
    try:
        data = json.loads(message)
        payload = data.get("data", data)  # fallback jika bukan format /stream

        symbol = payload.get("s")  # example: BTCUSDT
        price = float(payload.get("p", 0.0))
        event_ts = payload.get("E")

        if not symbol:
            return

        msg = {
            "symbol": symbol,
            "price": price,
            "timestamp": (event_ts / 1000) if event_ts else time.time(),
        }

        producer.send(TOPIC, msg)
        print(f"📩 Sent: {msg}")

    except Exception as e:
        print("❌ Error parsing message:", e)


def on_error(ws, error):
    print("❌ WS Error:", error)


def on_close(ws, close_status_code, close_msg):
    print("🔌 Connection Closed → reconnecting in 3s...")
    time.sleep(3)
    start_websocket()


def on_open(ws):
    print("🔗 Binance WebSocket Connected!")


def start_websocket():
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


if __name__ == "__main__":
    print("🚀 Producer WebSocket → Kafka started (BTC + ETH + BNB)...")
    start_websocket()
