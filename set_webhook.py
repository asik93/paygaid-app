import os
import requests

token = ""
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            if "TOKEN" in line.upper() and "=" in line:
                token = line.strip().split("=", 1)[1].strip('"').strip("'")

if token:
    webhook_url = "https://bot.paygaid.online/webhook"
    res = requests.get(f"https://api.telegram.org/bot{token}/setWebhook?url={webhook_url}")
    print("Webhook Response:", res.json())
else:
    print("Bot token not found!")
