from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes

# মিনি অ্যাপের সঠিক মেইন ড্যাশবোর্ড লিংক (ক্যাশ সমস্যা এড়াতে ?v=2 যুক্ত করা হয়েছে)
WEB_APP_URL = "https://asik93.github.io/paygaid-app/index.html?v=2"

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