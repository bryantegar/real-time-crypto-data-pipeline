import websocket
import time

def on_open(ws):
    print("🔥 CONNECTED to Binance WebSocket!")

def on_error(ws, error):
    print("🚫 WebSocket ERROR:", error)

def on_close(ws, close_status_code, close_msg):
    print("🔌 WebSocket CLOSED:", close_status_code, close_msg)

print("Trying to connect...")

ws = websocket.WebSocketApp(
    "wss://stream.binance.com:9443/ws/btcusdt@trade",
    on_open=on_open,
    on_error=on_error,
    on_close=on_close
)

ws.run_forever()
