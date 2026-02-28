import json
import time
from kafka import KafkaProducer
import websocket

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def on_message(ws, message):
    data = json.loads(message)
    event = {
        "symbol": "BTCUSDT",
        "price": float(data['p']),
        "volume": float(data['q']),
        "timestamp": data['T']
    }

    producer.send("crypto-realtime", event)
    print(f"📩 Sent → {event}")

def on_open(ws):
    print("🚀 Connected to Binance WebSocket Live Feed!")

def on_error(ws, error):
    print("❌ ERROR:", error)

def on_close(ws, close_status, close_msg):
    print("🔌 WebSocket Closed")

if __name__ == "__main__":
    socket = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    ws = websocket.WebSocketApp(socket, on_message=on_message, on_open=on_open, on_error=on_error, on_close=on_close)

    # Keep running forever
    ws.run_forever()
