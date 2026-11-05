path = "main.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# Vul ba invalid character gulo clean kore dewa hocche
code = code.replace("）", ")")

# Jodi ager broken routes thake ta bad dewa hocche
if "@app.get(\"/\")" in code:
    parts = code.split("@app.get(\"/\")")
    code = parts[0]

# Sothik ebong clean routes jog kora hocche
clean_routes = '''
from fastapi.responses import HTMLResponse
import os

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Mini App Frontend Not Found"

@app.get("/admin", response_class=HTMLResponse)
async def read_admin():
    admin_path = os.path.join(os.path.dirname(__file__), "static", "admin.html")
    if os.path.exists(admin_path):
        with open(admin_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Admin Panel HTML Not Found"
'''

code = code.strip() + "\n\n" + clean_routes.strip()

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Syntax fixed and routes added successfully!")
