import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from config import BOT_TOKEN
from page1_start import start_command

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # /start কমান্ডের জন্য হ্যান্ডলার
    app.add_handler(CommandHandler("start", start_command))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()