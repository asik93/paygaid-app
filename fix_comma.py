path = "main.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# Full-width comma ba character thakle ta replace kore sothik kora hocche
code = code.replace("，", ",")

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Comma fixed successfully!")
