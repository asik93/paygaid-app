import re

path = "/var/www/app/main.py"
with open(path, "r", encoding="utf-8") as f:
content = f.read()

# Remove any existing telegram_webhook definitions
content = re.sub(r'@app\.post\("/webhook"\)\s*async def telegram_webhook.*?(?=\n@|\n[a-zA-Z]|\Z)', '', content, flags=EE|re.S if 'EE' in globals() else re.DOTALL)
# Simpler cleanup by lines
lines = content.splitlines()
clean_lines = []
skip = False
for line in lines:
if "@app.post(\"/webhook\")" in line or "async def telegram_webhook" in line:
    skip = True
    continue
if skip:
    if line.strip() == "" or line.startswith("    ") or line.startswith("\t"):
        continue
    else:
        skip = False
clean_lines.append(line)

# Append correct webhook
clean_lines.append("\n@app.post(\"/webhook\")")
clean_lines.append("async def telegram_webhook(request: Request):")
clean_lines.append("    data = await request.json()")
clean_lines.append("    return {\"status\": \"ok\"}\n")

with open(path, "w", encoding="utf-8") as f:
f.write("\n".join(clean_lines))

print("Successfully fixed main.py")
