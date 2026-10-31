from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

# Apnar VPS IP address diye live domain link update kora holo
WEB_APP_URL = "https://66.29.134.253"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🚀 Open PayGaid Portal", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "<b>Welcome to PayGaid Network</b>\n\n"
        "Click the button below to launch the portal."
    )

    await update.message.reply_text(
        text=welcome_text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )