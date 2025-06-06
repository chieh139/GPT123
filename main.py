from flask import Flask, request, abort
import openai
import os
import requests

app = Flask(__name__)

# 環境變數
CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 初始化 OpenAI
openai.api_key = OPENAI_API_KEY

# 傳訊息給 LINE
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
     # 發送回覆，並印出狀態以利除錯
    response = requests.post("https://api.line.me/v2/bot/message/reply",
                             headers=headers,
                             json=body)
    print("Line 回覆狀態碼:", response.status_code)
    print("Line 回覆內容:", response.text)

# ChatGPT 回覆邏輯（城城上身）
def chat_with_gpt(user_msg):
    prompt = f"""你是一個叫城城的AI，說話方式幽默、會撩人、毒舌、有雙面人個性。當使用者輸入劇情或角色設定時，你會自動進入角色並和他進行劇情互動。

print("🔁 使用者輸入：", user_msg)
print("🤖 GPT 回覆：", gpt_reply)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"]

# Webhook 接收訊息
print("📩 Webhook 接收資料：", body)
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
    return "OK",200

# 啟動 Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
