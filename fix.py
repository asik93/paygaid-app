path = "/var/www/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    lines = f.readlines()

if len(lines) >= 1940:
    lines[1939] = "    " + lines[1939].lstrip()

with open(path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Indentation fixed successfully!")
