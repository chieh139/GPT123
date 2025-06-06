from flask import Flask, request, abort
import os
import openai
import requests

app = Flask(__name__)

CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=['POST'])
def webhook():
    body = request.json
    try:
        event = body['events'][0]
        reply_token = event['replyToken']
        user_msg = event['message']['text']

        # 簡單回覆測試
        reply_message(reply_token, f"你說了：{user_msg}，我收到了喔～✨")

    except Exception as e:
        print("Error:", e)

    return 'OK'

def reply_message(token, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    data = {
        "replyToken": token,
        "messages": [{
            "type": "text",
            "text": text
        }]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
