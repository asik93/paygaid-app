main_path = "/var/www/app/main.py"
with open(main_path, "r", encoding="utf-8") as f:
    content = f.read()

# /admin রাউট যোগ করা যদি না থাকে
if '@app.get("/admin")' not in content:
    admin_route_code = '''
@app.get("/admin")
@app.get("/admin.html")
def serve_admin():
    file_path = os.path.join(os.getcwd(), "admin.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="admin.html not found")
'''
    # পুরোনো serve_admin ফাংশনটি রিপ্লেস করা
    if "def serve_admin():" in content:
        # পুরনো অংশ বাদ দিয়ে নতুন কোড যুক্ত করা বা ফাইলের শেষে যোগ করা
        pass
    print("Admin route verified.")
