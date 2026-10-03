import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# GitHub Pages URL
WEB_APP_URL = "https://asik93.github.io/paygaid-app/"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # সরাসরি মিনি অ্যাপ খোলার বাটন
    keyboard = [
        [InlineKeyboardButton("🚀 Open PayGaid Portal", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_text = (
        "**Welcome to PayGaid Agent Portal**\n\n"
        "Click the button below to launch the portal:"
    )
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

if __name__ == '__main__':
    # আপনার নতুন সঠিকভাবে দেওয়া বট টোকেন
    app = ApplicationBuilder().token("8661674837:AAHoVp-p9o8mydFq7UQY08mcDHppG_wbfI4").build()
    
    app.add_handler(CommandHandler("start", start))
    
    print("Bot is running...")
    app.run_polling()