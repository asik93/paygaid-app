path = "main.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# Jodi ager vul routes thake ta bad dewa hocche
if "@app.get(\"/\")" in code:
    code = code.split("@app.get(\"/\")")[0]

# Sothik static folder mount ebong absolute path diye routes define kora hocche
new_routes = '''
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os

# Static folder mount kora hocche jate css/js/images load hoy
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = os.path.abspath(os.path.join("static", "index.html"))
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h3>index.html not found in static folder!</h3>", status_code=404)

@app.get("/admin", response_class=HTMLResponse)
async def read_admin():
    admin_path = os.path.abspath(os.path.join("static", "admin.html"))
    if os.path.exists(admin_path):
        with open(admin_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h3>admin.html not found in static folder!</h3>", status_code=404)
'''

code = code.strip() + "\n\n" + new_routes.strip()

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Static paths fixed successfully!")
