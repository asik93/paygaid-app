with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

webhook_code = '''
from fastapi import Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

WEB_APP_URL = "https://bot.paygaid.online"

@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        if "message" in data and "text" in data["message"]:
            text = data["message"]["text"]
            chat_id = data["message"]["chat"]["id"]
            if text.startswith("/start"):
                keyboard = [[InlineKeyboardButton("Open Portal", web_app=WebAppInfo(url=WEB_APP_URL))]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await bot.send_message(
                    chat_id=chat_id,
                    text="Welcome to PayGaid Agent Portal!\\nPlease click the 'Open Portal' button below to proceed.",
                    reply_markup=reply_markup
                )
        return {"status": "ok"}
    except Exception as e:
        print("Webhook error:", e)
        return {"status": "error", "message": str(e)}
'''

if "/webhook" not in content:
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content + "\n" + webhook_code)
    print("Webhook endpoint successfully added to main.py!")
else:
    print("Webhook endpoint already exists.")
