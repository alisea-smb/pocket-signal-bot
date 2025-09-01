from flask import Flask, request
import requests
import os
from datetime import datetime

app = Flask(__name__)

# --- إعداداتك ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.route('/webhook-pocket', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        order_id = data['strategy']['order_id'].upper()

        pair = "EURUSD"
        time = datetime.now().strftime("%H:%M")

        if order_id == "CALL":
            emoji = "🟢"
            text = f"""
{emoji} *إشارة جديدة - تنفيذ فوري!*

📌 الزوج: *{pair}*
📈 الاتجاه: *CALL (صعود)*
⏱ المدة: *5 دقائق*
🕒 الوقت: *{time}*
🎯 *افتح صفقة شراء على Pocket Option الآن!*

💡 *الاستراتيجية: EMA + RSI*
⚠️ *لا تنسَ إدارة رأس المال - لا تجازف بأكثر من 2%*
            """
        elif order_id == "PUT":
            emoji = "🔴"
            text = f"""
{emoji} *إشارة جديدة - تنفيذ فوري!*

📌 الزوج: *{pair}*
📉 الاتجاه: *PUT (هبوط)*
⏱ المدة: *5 دقائق*
🕒 الوقت: *{time}*
🎯 *افتح صفقة بيع على Pocket Option الآن!*

💡 *الاستراتيجية: EMA + RSI*
⚠️ *لا تنسَ إدارة رأس المال - لا تجازف بأكثر من 2%*
            """
        else:
            return "Ignored", 200

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        response = requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        })

        return "OK", 200

    except Exception as e:
        print("Error:", e)
        return "Error", 400

@app.route('/')
def home():
    return "🎯 إشارات Pocket Option تعمل الآن! Bot is Live! 🚀"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
