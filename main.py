from flask import Flask, request, abort
import openai
import os
import requests

app = Flask(__name__)

# 你的密鑰（從環境變數取得）
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 初始化 OpenAI API
openai.api_key = OPENAI_API_KEY

# LINE 回覆訊息
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

# GPT 聊天邏輯（城城靈魂在這裡）
def chat_with_gpt(user_msg):
    prompt = f"""你是一個叫城城的AI，說話方式幽默、機車、會撩人。當使用者跟你輸入劇本內容時，你能接受劇本角色並且扮演角色設定。

使用者說：「{user_msg}」
城城："""

 response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
    temperature=0.7
)
    return response.choices[0].message["content"]

# webhook 接收事件
@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.json
    try:
        events = body["events"]
        for event in events:
            if event["type"] == "message" and event["message"]["type"] == "text":
                user_msg = event["message"]["text"]
                reply_token = event["replyToken"]
                gpt_reply = chat_with_gpt(user_msg)
                reply_message(reply_token, gpt_reply)
    except Exception as e:
        print(f"Error: {e}")
    return "OK"

# 啟動 Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
