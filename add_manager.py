from pydantic import BaseModel
from typing import Optional

# These will be appended safely
manager_code = """

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

with open("/var/www/app/main.py", "a", encoding="utf-8") as f:
    f.write(manager_code)

print("Manager API appended successfully via script!")
