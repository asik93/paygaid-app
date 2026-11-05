import os

file_path = "/var/www/app/main.py"
clean_code = """import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

app = FastAPI(
    title="PayGaid Agent Portal API",
    description="Backend API for managing agents, applications, verification, and authentication.",
    version="1.0.0"
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN and os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                if "TOKEN" in k.upper():
                    TOKEN = v.strip().strip('"').strip("'")

WEB_APP_URL = "https://bot.paygaid.online"
telegram_app = None

@app.on_event("startup")
async def startup_event():
    global telegram_app
    if TOKEN:
        telegram_app = Application.builder().token(TOKEN).updater(None).build()
        
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            keyboard = [[InlineKeyboardButton("Open Portal", web_app=WebAppInfo(url=WEB_APP_URL))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if update.message:
                await update.message.reply_text(
                    "Welcome to PayGaid Agent Portal!\\nPlease click the 'Open Portal' button below to proceed.",
                    reply_markup=reply_markup
                )

        telegram_app.add_handler(CommandHandler("start", start))
        await telegram_app.initialize()
        print("Telegram application initialized successfully.")

@app.on_event("shutdown")
async def shutdown_event():
    global telegram_app
    if telegram_app:
        await telegram_app.shutdown()

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    file_path = "index.html"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return "index.html not found"

@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    file_path = "admin.html"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return "admin.html not found"

@app.post("/webhook")
async def telegram_webhook(request: Request):
    global telegram_app
    try:
        data = await request.json()
        if telegram_app:
            update = Update.de_json(data, telegram_app.bot)
            await telegram_app.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error", "message": str(e)}
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(clean_code)
print("main.py updated successfully via script!")
