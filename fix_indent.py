path = "/var/www/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Remove any previous manager code blocks to ensure a fresh start
if "ManagerVerifySchema" in text:
    parts = text.split("class ManagerVerifySchema")
    text = parts[0].strip()

# Clean code block with strictly normalized indentation (no leading spaces on top-level definitions)
clean_api_code = """
class ManagerVerifySchema(BaseModel):
    username: str
    status: Optional[str] = "Verified"

@app.get("/api/admin/managers-list")
def get_admin_managers_list(db: Session = Depends(get_db)):
    managers = db.query(models.ManagerVerification).all()
    return [{"id": m.id, "username": m.username, "status": m.status} for m in managers]

@app.post("/api/admin/managers-list")
def add_or_update_manager(data: ManagerVerifySchema, db: Session = Depends(get_db)):
    clean_uname = data.username.strip().replace("@", "").lower()
    existing = db.query(models.ManagerVerification).filter(models.ManagerVerification.username == clean_uname).first()
    if existing:
        existing.status = data.status
    else:
        new_m = models.ManagerVerification(username=clean_uname, status=data.status)
        db.add(new_m)
    db.commit()
    return {"status": "success", "message": "Manager saved successfully"}

@app.delete("/api/admin/managers-list/{manager_id}")
def delete_manager_item(manager_id: int, db: Session = Depends(get_db)):
    m = db.query(models.ManagerVerification).filter(models.ManagerVerification.id == manager_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Manager not found")
    db.delete(m)
    db.commit()
    return {"status": "success", "message": "Manager deleted successfully"}

@app.get("/api/check-manager/{username}")
def check_telegram_manager(username: str, db: Session = Depends(get_db)):
    clean_uname = username.strip().replace("@", "").lower()
    m = db.query(models.ManagerVerification).filter(models.ManagerVerification.username == clean_uname).first()
    if m:
        return {"status": "success", "verified": m.status == "Verified", "manager_status": m.status, "username": clean_uname}
    else:
        return {"status": "success", "verified": False, "manager_status": "Scammer", "username": clean_uname}
"""

# Strip leading/trailing whitespaces from each line to prevent unexpected indentation
normalized_code = "\n".join([line.rstrip() for line in clean_api_code.strip().splitlines()])

with open(path, "w", encoding="utf-8") as f:
    f.write(text + "\n\n" + normalized_code + "\n")

print("Normalized indentation and updated successfully!")
