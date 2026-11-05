with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# পুরানো ওয়েভহুক ব্লকটি সরিয়ে নতুন এবং নির্ভুল হ্যান্ডলার যোগ করা
if '@app.post("/webhook")' in content:
    # ওয়েভহুকের আগের কোড পর্যন্ত রেখে বাকিটা বাদ দেওয়া
    content = content.split('@app.post("/webhook")')[0]

new_webhook = '''
from fastapi import Request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, Bot
import os

TELEGRAM_BOT_TOKEN = "8661674837:AAEoV7JSVWumM2ozCPdOYgBkj2omDEpBZfg"
bot = Bot(token=TELEGRAM_BOT_TOKEN)
WEB_APP_URL = "https://bot.paygaid.online"

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        print("Received update:", data)
        if "message" in data:
            msg = data["message"]
            chat_id = msg["chat"]["id"]
            text = msg.get("text", "")
            
            # /start বা অন্য যেকোনো কমান্ডে ওয়েলকাম মেসেজ ও মিনি অ্যাপ বাটন পাঠানো
            keyboard = [[InlineKeyboardButton("Open Portal", web_app=WebAppInfo(url=WEB_APP_URL))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await bot.send_message(
                chat_id=chat_id,
                text="Welcome to PayGaid Agent Portal! Please click the 'Open Portal' button below to launch the application.",
                reply_markup=reply_markup
            )
        return {"status": "ok"}
    except Exception as e:
        print("Webhook error:", e)
        return {"status": "error", "message": str(e)}
'''

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content + "\n" + new_webhook)

print("Handler updated successfully!")
