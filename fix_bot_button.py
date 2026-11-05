import os

path = "main.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# যদি main.py ফাইলে web_app বা WebAppInfo না থাকে, তবে কোড আপডেট করা
if "WebAppInfo" not in content:
    # টেলিগ্রাম বটের স্টার্ট হ্যান্ডলার ও ওয়েব অ্যাপ বাটন কোড বসানো
    new_code = '''
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

WEB_APP_URL = "https://bot.paygaid.online"

# স্টার্ট কমান্ড হ্যান্ডলার আপডেট
@dp.message(Command("start"))
async def start_command(message: types.Message):
    keyboard = [[InlineKeyboardButton("Open Portal", web_app=WebAppInfo(url=WEB_APP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await message.answer(
        "Welcome to PayGaid Agent Portal!\\nPlease click the 'Open Portal' button below to proceed.",
        reply_markup=reply_markup
    )
'''
    # ফাইলের শেষে বা উপযুক্ত স্থানে যোগ করা
    content += "\n\n" + new_code
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("main.py updated with WebAppInfo successfully!")
else:
    print("WebAppInfo already exists in main.py")
