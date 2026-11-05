import os
import requests

# আপনার বটের টোকেন এবং ডোমেইন অনুযায়ী সঠিক ওয়েভহুক ইউআরএল
# (যদি পরিবেশ ভেরিয়েবলে টোকেন থাকে অথবা সরাসরি কোড থেকে রিড করে)
try:
    with open("main.py", "r") as f:
        content = f.read()
except Exception:
    pass

# টেলিগ্রাম API দিয়ে সরাসরি ওয়েভহুক সেট করা (bot.paygaid.online/webhook)
# আপনার টোকেনটি নিচে বসিয়ে নিতে পারেন অথবা এনভায়রনমেন্ট থেকে নিতে পারে
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE") 
WEBHOOK_URL = "https://bot.paygaid.online/webhook"

# সরাসরি টেলিগ্রাম সেট ওয়েভহুক রিকোয়েস্ট পাঠানো
print("Updating webhook to:", WEBAPP_URL if 'WEBAPP_URL' in locals() else WEBHOOK_URL)
