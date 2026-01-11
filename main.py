import os
from flask import Flask, request, jsonify
from binance.client import Client

app = Flask(__name__)

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
testnet = os.getenv("BINANCE_TESTNET", "false").lower() == "true"

client = Client(api_key, api_secret)

if testnet:
    client.API_URL = "https://testnet.binance.vision/api"

@app.route("/")
def home():
    return "Bot running (testnet)"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    symbol = data.get("symbol", "BTCUSDT")
    side = data.get("side", "BUY")
    usd = float(data.get("usd", 10))

    order = client.create_order(
        symbol=symbol,
        side=side,
        type="MARKET",
        quoteOrderQty=usd
    )

    return jsonify(order)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

