import websocket

def on_open(ws):
    print("CONNECTED TO BINANCE WEBSOCKET!")

ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/btcusdt@trade", on_open=on_open)
ws.run_forever()
