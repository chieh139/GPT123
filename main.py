from flask import Flask, request, abort
import openai
import os

app = Flask(__name__)

CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json
    # 簡化的訊息處理邏輯
    return "OK"

if __name__ == "__main__":
    app.run()
