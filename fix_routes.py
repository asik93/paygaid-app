path = "main.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# Jodi root ebong admin HTML route gulo na thake ta add kore dewa hocche
routes_code = '''
from fastapi.responses import HTMLResponse
import os

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = os.path.join(os.path.dirname(__file）， "static", "index.html")
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

if "@app.get(\"/admin\")" not in code:
    code = code + "\n\n" + routes_code

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Routes added successfully!")
