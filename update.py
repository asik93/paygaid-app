path = "/var/www/app/main.py"
with open(path, "r", encoding="utf-8") as f:
lines = f.readlines()

new_lines = []
skip = False
for line in lines:
if "@app.post(\"/webhook\")" in line or "async def telegram_webhook" in line:
    skip = True
    continue
if skip:
    if line.startswith("    ") or line.startswith("\t") or line.strip() == "":
        continue
    else:
        skip = False
new_lines.append(line)

new_lines.append("\n@app.post(\"/webhook\")\n")
new_lines.append("async def telegram_webhook(request: Request):\n")
new_lines.append("    data = await request.json()\n")
new_lines.append("    return {\"status\": \"ok\"}\n")

with open(path, "w", encoding="utf-8") as f:
f.writelines(new_lines)

print("SUCCESS")
