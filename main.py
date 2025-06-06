from flask import Flask, request, abort
import openai
import os
import requests

app = Flask(__name__)

CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

@app.route("/webhook", methods=['POST'])
def webhook():
    body = request.json
    for event in body['events']:
        if event['type'] == 'message' and event['message']['type'] == 'text':
            user_message = event['message']['text']
            reply_token = event['replyToken']
            reply = chat_with_gpt(user_message)
            reply_message(reply_token, reply)
    return 'OK'

def chat_with_gpt(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            { "role": "system", "content": "你是一位親切會撒嬌、聰明機靈、叫城城的聊天助手。" },
            { "role": "user", "content": user_message }
        ]
    )
    return response['choices'][0]['message']['content']

def reply_message(reply_token, text):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    body = {
        "replyToken": reply_token,
        "messages": [{
            "type": "text",
            "text": text
        }]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=body)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
