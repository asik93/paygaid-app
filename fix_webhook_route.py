import os

path = "main.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# যদি /webhook রুট না থাকে, তবে FastAPI তে একটি সিম্পল ওয়েভহুক রুট যোগ করা
if "@app.post(\"/webhook\")" not in content and "@app.post('/webhook')" not in content:
    webhook_code = '''

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    # Telegram update handle logic
    return {"status": "ok"}
'''
    content += webhook_code
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Webhook route added to main.py successfully!")
else:
    print("Webhook route already exists in main.py")
