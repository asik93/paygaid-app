path = "/var/www/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()
if "/webhook" not in code:
    with open(path, "a", encoding="utf-8") as f:
        f.write("\n\n@app.post(\"/webhook\")\nasync def telegram_webhook(request: Request):\n    data = await request.json()\n    return {\"status\": \"ok\"}\n")
    print("Webhook added!")
else:
    print("Already exists!")
