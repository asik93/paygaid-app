import random
import os
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

app = FastAPI(
    title="PayGaid Agent Portal API",
    description="Backend API for managing agents, applications, verification, and authentication.",
    version="1.0.0"
)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN and os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                if "TOKEN" in k.upper():
                    TOKEN = v.strip().strip('"').strip("'")

WEB_APP_URL = "https://bot.paygaid.online"
telegram_app = None

@app.on_event("startup")
async def startup_event():
    global telegram_app
    if TOKEN:
        telegram_app = Application.builder().token(TOKEN).updater(None).build()
        
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            keyboard = [[InlineKeyboardButton("Open Portal", web_app=WebAppInfo(url=WEB_APP_URL))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            if update.message:
                await update.message.reply_text(
                    "Welcome to PayGaid Agent Portal!\nPlease click the 'Open Portal' button below to proceed.",
                    reply_markup=reply_markup
                )

        telegram_app.add_handler(CommandHandler("start", start))
        await telegram_app.initialize()
        print("Telegram application initialized successfully.")

@app.on_event("shutdown")
async def shutdown_event():
    global telegram_app
    if telegram_app:
        await telegram_app.shutdown()

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    file_path = "index.html"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return "index.html not found"

@app.get("/admin", response_class=HTMLResponse)
async def admin_page():
    file_path = "admin.html"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return "admin.html not found"

@app.post("/webhook")
async def telegram_webhook(request: Request):
    global telegram_app
    try:
        data = await request.json()
        if telegram_app:
            update = Update.de_json(data, telegram_app.bot)
            await telegram_app.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    # Prothome agent-dashboard ba country selection page khuje set kora
    for fname in ["agent-dashboard.html", "index.html"]:
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8") as file:
                html_content = file.read()
                if "Select your Country" in html_content or "Country" in html_content:
                    return html_content
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as file:
            return file.read()
    return "Page not found"

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    # Prothome country selection ba page1 file khuje ber kora
    for fname in ["page1_start.html", "index.html", "agent-dashboard.html"]:
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8") as file:
                html_content = file.read()
                if "Select your Country" in html_content:
                    return html_content
    # Jodi file na paoa jay tahole index.html return korbe
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as file:
            return file.read()
    return "Page not found"


    file_path = os.path.join(os.getcwd(), "admin.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="admin.html not found")


@app.get("/admin")
def serve_admin_alias():
    import os
    from fastapi.responses import FileResponse
    from fastapi import HTTPException
    fp = os.path.join(os.getcwd(), "admin.html")
    if os.path.exists(fp):
        return FileResponse(fp)
    raise HTTPException(status_code=404, detail="admin.html not found")



@app.post("/api/admin/login")
def admin_login_api(data: dict):
    pwd = data.get("password", "")
    if pwd == "admin123":
        return {"status": "success", "message": "Admin login successful"}
    from fastapi import HTTPException
    raise HTTPException(status_code=401, detail="Incorrect admin password")



@app.get("/api/agents")
def get_all_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    agents = db.query(models.Agent).order_by(models.Agent.id.desc()).offset(skip).limit(limit).all()
    result = []
    for ag in agents:
        disp_id = ag.agent_username if (ag.agent_username and ag.agent_username.strip() != "") else ag.application_id
        
        current_bal = 0.0
        for col in ["opening_balance", "balance"]:
            if hasattr(ag, col) and getattr(ag, col) is not None:
                try:
                    current_bal = float(getattr(ag, col))
                    break
                except:
                    pass

        currency_sym = COUNTRY_CURRENCY_MAP.get(ag.country, getattr(ag, "currency_symbol", "৳"))

        result.append({
            "id": ag.id,
            "application_id": ag.application_id,
            "agent_id": disp_id,
            "full_name": ag.full_name,
            "email": ag.email,
            "email_address": ag.email,
            "mobile": ag.mobile,
            "phone_number": ag.mobile,
            "whatsapp": ag.whatsapp,
            "telegram": ag.telegram,
            "country": ag.country,
            "currency_symbol": currency_sym,
            "payment_gateway": ag.payment_gateway,
            "account_number": ag.account_number,
            "doc_type": ag.doc_type,
            "doc_number": ag.doc_number,
            "front_image": ag.front_image or "front.jpg",
            "back_image": ag.back_image or "back.jpg",
            "assigned_manager": ag.assigned_manager,
            "message": ag.message,
            "deposit_limit_status": ag.deposit_limit_status,
            "withdrawal_limit_status": ag.withdrawal_limit_status,
            "security_deposit_status": ag.security_deposit_status,
            "balance": current_bal,
            "status": ag.status or "Pending",
            "language": ag.language
        })
    return result




from fastapi import FastAPI, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
import random

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/agents/register", status_code=201)
async def register_agent(request: Request, db: Session = Depends(get_db)):
    try:
        if request.headers.get("content-type", "").startswith("application/json"):
            data = await request.json()
        else:
            form = await request.form()
            data = dict(form)
    except Exception:
        data = {}

    full_name = data.get("full_name") or data.get("fullName") or data.get("name") or "Agent Applicant"
    email = data.get("email") or data.get("email_address") or f"agent_{random.randint(1000,9999)}@gmail.com"
    mobile = data.get("mobile") or data.get("phone") or data.get("phone_number") or ""
    whatsapp = data.get("whatsapp") or ""
    telegram = data.get("telegram") or ""
    country = data.get("country") or "Bangladesh"
    language = data.get("language") or "English"
    payment_gateway = data.get("payment_gateway") or data.get("wallet_name") or "N/A"
    account_number = data.get("account_number") or data.get("wallet_account_number") or "N/A"
    doc_type = data.get("doc_type") or "NID Card"
    doc_number = data.get("doc_number") or "N/A"
    front_image = data.get("front_image") or "front.jpg"
    back_image = data.get("back_image") or "back.jpg"

    app_id = generate_application_id()
    while db.query(models.Agent).filter(models.Agent.application_id == app_id).first():
        app_id = generate_application_id()

    c_symbol = COUNTRY_CURRENCY_MAP.get(country, "৳")

    new_agent = models.Agent(
        application_id=app_id,
        country=country,
        currency_symbol=c_symbol,
        language=language,
        full_name=full_name,
        email=email,
        mobile=mobile,
        whatsapp=whatsapp,
        telegram=telegram,
        payment_gateway=payment_gateway,
        account_number=account_number,
        doc_type=doc_type,
        doc_number=doc_number,
        front_image=front_image,
        back_image=back_image,
        status="Pending",
        created_at=get_local_time(country)
    )

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    disp_id = new_agent.agent_username if (new_agent.agent_username and new_agent.agent_username.strip() != "") else new_agent.application_id

    return {
        "status": "success",
        "message": "Application submitted successfully",
        "application_id": new_agent.application_id,
        "agent_id": disp_id,
        "full_name": new_agent.full_name
    }