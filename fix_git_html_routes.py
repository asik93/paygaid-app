path = "main.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# পুরানো রুটগুলো পরিষ্কার করে দেওয়া হচ্ছে
if "@app.get(\"/admin\")" in code:
    code = code.split("@app.get(\"/admin\")[0]") # safe split

# সঠিক পাথ দিয়ে রুটগুলো যুক্ত করা হচ্ছে
new_routes = '''
from fastapi.responses import HTMLResponse
import os

@app.get("/", response_class=HTMLResponse)
async def read_index():
    # সরাসরি রুট ফোল্ডারে থাকা index.html অথবা accounts-manager.html রিড করবে
    for fname in ["index.html", "accounts-manager.html", "add-money.html"]:
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8") as f:
                return f.read()
    return "Frontend HTML Not Found"

@app.get("/admin", response_class=HTMLResponse)
async def read_admin():
    # সরাসরি রুট ফোল্ডারে থাকা admin.html রিড করবে
    admin_path = "admin.html"
    if os.path.exists(admin_path):
        with open(admin_path, "r", encoding="utf-8") as f:
            return f.read()
    return HTMLResponse("<h3>admin.html not found in root directory!</h3>", status_code=404)
'''

# যদি রাউটগুলো অলরেডি না থাকে তবে যোগ করা
if "@app.get(\"/admin\")" not in code:
    code = code + "\n\n" + new_routes

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Git HTML routes fixed successfully!")
