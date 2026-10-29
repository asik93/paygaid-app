from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, or_
import random
import string
import requests
import os
from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta, timezone

from database import engine, Base, get_db
import models

# Telegram Bot Config
TELEGRAM_BOT_TOKEN = "8661674837:AAF5_dKDGeEWqHKgQmIblYQwSJPyAfCjYtU"

COUNTRY_CURRENCY_MAP = {
    "India": "₹",
    "Pakistan": "₨",
    "UAE": "AED",
    "Saudi Arabia": "ر.س",
    "Bangladesh": "৳",
    "Nepal": "रू",
    "Philippines": "₱",
    "Vietnam": "₫",
    "Thailand": "฿",
    "Malaysia": "RM",
    "Indonesia": "Rp",
    "Qatar": "QR"
}

COUNTRY_TIMEZONE_OFFSETS = {
    "India": 5.5,
    "Pakistan": 5.0,
    "UAE": 4.0,
    "Saudi Arabia": 3.0,
    "Bangladesh": 6.0,
    "Nepal": 5.75,
    "Philippines": 8.0,
    "Vietnam": 7.0,
    "Thailand": 7.0,
    "Malaysia": 8.0,
    "Indonesia": 7.0,
    "Qatar": 3.0
}

def get_local_time(country: Optional[str] = "Bangladesh") -> datetime:
    utc_now = datetime.now(timezone.utc).replace(tzinfo=None)
    offset_hours = COUNTRY_TIMEZONE_OFFSETS.get(country, 6.0)
    return utc_now + timedelta(hours=offset_hours)

class Withdrawal(Base):
    __tablename__ = "withdrawals"
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, index=True)
    full_name = Column(String)
    method = Column(String)
    amount = Column(Float)
    commission_rate = Column(Float, default=0.0)
    commission_amount = Column(Float, default=0.0)
    wallet_address = Column(String)
    status = Column(String, default="Pending")
    rejection_reason = Column(String, nullable=True)
    assigned_agent_id = Column(String, nullable=True, index=True)
    request_type = Column(String, default="agent_withdrawal", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AgentGateway(Base):
    __tablename__ = "agent_gateways"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    region = Column(String, default="India")
    type = Column(String)
    name = Column(String)
    details = Column(String)
    min = Column(String)
    max = Column(String)
    badge = Column(String)
    active = Column(Boolean, default=True)

class ContactSupportMessage(Base):
    __tablename__ = "contact_support_messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    subject = Column(String, default="Support Query")
    message = Column(String)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)

class SystemSetting(Base):
    __tablename__ = "system_settings"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    value = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PayGaid Agent Portal API",
    description="Backend API for managing agents, applications, verification, and authentication.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

verified_managers_db = [
    {"id": 1, "username": "manager01"},
    {"id": 2, "username": "manager02"},
    {"id": 3, "username": "paygaid"}
]

class SupportSettingsSchema(BaseModel):
    telegram_link: str
    support_email: str

class ContactMessageSchema(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    subject: Optional[str] = "Support Query"
    message: str

class ManagerSchema(BaseModel):
    id: int
    username: str

class ManualAgentRegisterRequest(BaseModel):
    full_name: str
    agent_id: str
    phone_number: str
    email_address: EmailStr
    registration_date: Optional[str] = datetime.now().strftime("%d %b, %Y")
    country: str
    currency_symbol: Optional[str] = "৳"
    wallet_name: str
    wallet_account_number: str
    opening_balance: float
    password: str
    confirm_password: str
    manager_telegram: Optional[str] = ""

class CryptoGatewayUpdateSchema(BaseModel):
    symbol: str
    wallet_address: str
    min_deposit: str

class GatewaySchema(BaseModel):
    username: str
    region: Optional[str] = "India"
    type: str
    name: str
    details: str
    min: str
    max: str
    badge: str
    active: Optional[bool] = True

class BalanceUpdateSchema(BaseModel):
    amount: float

class AdminUpdatePayload(BaseModel):
    status: Optional[str] = None
    assigned_manager: Optional[str] = None
    message: Optional[str] = None
    deposit_limit_status: Optional[str] = None
    withdrawal_limit_status: Optional[str] = None
    security_deposit_status: Optional[str] = None
    full_name: Optional[str] = None
    agent_id: Optional[str] = None
    mobile: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    email_address: Optional[str] = None
    balance: Optional[float] = None
    password: Optional[str] = None

class CreateWithdrawRequestSchema(BaseModel):
    agent_id: str
    amount: float
    commission_rate: float
    method: str
    serial_id: str
    wallet_address: str

class ChangePasswordSchema(BaseModel):
    username: Optional[str] = None
    agent_id: Optional[str] = None
    current_password: str
    new_password: str

class ForgotPasswordRequestSchema(BaseModel):
    method: str
    target: str

class ResetPasswordWithOTPSchema(BaseModel):
    target: str
    otp_code: str
    new_password: str

class AdminLoginSchema(BaseModel):
    password: str

class AdminChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str

def generate_application_id():
    return "PG-AG-" + "".join(random.choices(string.digits, k=6))

def get_agent_currency(db: Session, agent_id: str) -> str:
    agent = db.query(models.Agent).filter(
        (models.Agent.agent_username == agent_id) | 
        (models.Agent.application_id == agent_id)
    ).first()
    if agent:
        if agent.country in COUNTRY_CURRENCY_MAP:
            return COUNTRY_CURRENCY_MAP[agent.country]
        if hasattr(agent, "currency_symbol") and agent.currency_symbol:
            return agent.currency_symbol
    return "RM"

def seed_defaults(db: Session):
    if db.query(models.CryptoGateway).count() == 0:
        default_gateways = [
            models.CryptoGateway(
                symbol="TRON", name="TRON (TRX)", wallet_address="TRX9Y2khEsLJW1ChVWFMSMeRDow5KcbL39",
                min_deposit="600 TRX", exchange_rate="Live Rate",
                icon_html="<img src='https://assets.coingecko.com/coins/images/1094/large/tron-logo.png' alt='TRON' style='width:24px;height:24px;object-fit:contain;display:inline-block;'>", unique_code="(x123-48)"
            ),
            models.CryptoGateway(
                symbol="USDT_TRON", name="Tether on Tron", wallet_address="TQn9Y2khEsLJW1ChVWFMSMeRDow5KcbLSE",
                min_deposit="200 USDT", exchange_rate="Live Rate",
                icon_html="<img src='https://assets.coingecko.com/coins/images/325/large/Tether.png' alt='USDT' style='width:22px;height:22px;object-fit:contain;display:inline-block;'><img src='https://assets.coingecko.com/coins/images/1094/large/tron-logo.png' alt='TRON' style='width:22px;height:22px;object-fit:contain;display:inline-block;margin-left:-4px;'>", unique_code="(x124-52)"
            ),
            models.CryptoGateway(
                symbol="USDT_BSC", name="Tether on BSC", wallet_address="0x874f3d481132dd70ec9c63851bb2e1556dc7a8d",
                min_deposit="200 USDT", exchange_rate="Live Rate",
                icon_html="<img src='https://assets.coingecko.com/coins/images/325/large/Tether.png' alt='USDT' style='width:22px;height:22px;object-fit:contain;display:inline-block;'><img src='https://assets.coingecko.com/coins/images/825/large/bnb-icon2_2x.png' alt='BSC' style='width:22px;height:22px;object-fit:contain;display:inline-block;margin-left:-4px;'>", unique_code="(x125-99)"
            ),
            models.CryptoGateway(
                symbol="USDT_ETH", name="Tether on Ethereum", wallet_address="0x7169D381015D7A9a47738228148b1114b0b147B2",
                min_deposit="200 USDT", exchange_rate="Live Rate",
                icon_html="<img src='https://assets.coingecko.com/coins/images/325/large/Tether.png' alt='USDT' style='width:22px;height:22px;object-fit:contain;display:inline-block;'><img src='https://assets.coingecko.com/coins/images/279/large/ethereum.png' alt='ETH' style='width:22px;height:22px;object-fit:contain;display:inline-block;margin-left:-4px;'>", unique_code="(x126-11)"
            ),
            models.CryptoGateway(
                symbol="LTC", name="Litecoin", wallet_address="LTC7Y2khEsLJW1ChVWFMSMeRDow5KcbL39",
                min_deposit="0.05 LTC", exchange_rate="Live Rate",
                icon_html="<img src='https://assets.coingecko.com/coins/images/2/large/litecoin.png' alt='Litecoin' style='width:24px;height:24px;object-fit:contain;display:inline-block;'>", unique_code="(x127-88)"
            ),
            models.CryptoGateway(
                symbol="BTC", name="Bitcoin", wallet_address="1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
                min_deposit="0.005822 BTC", exchange_rate="Live Rate",
                icon_html="<img src='https://assets.coingecko.com/coins/images/1/large/bitcoin.png' alt='Bitcoin' style='width:24px;height:24px;object-fit:contain;display:inline-block;'>", unique_code="(x128-03)"
            )
        ]
        db.add_all(default_gateways)

    if not db.query(SystemSetting).filter(SystemSetting.key == "telegram_link").first():
        db.add(SystemSetting(key="telegram_link", value="https://t.me/PayGaidSupport"))
    if not db.query(SystemSetting).filter(SystemSetting.key == "support_email").first():
        db.add(SystemSetting(key="support_email", value="support@paygaid.com"))

    db.commit()

@app.on_event("startup")
def startup_event():
    db = next(get_db())
    try:
        seed_defaults(db)
    except Exception as e:
        print("Startup seed error:", e)
    finally:
        db.close()

@app.get("/api/agent/gateways/{username}")
def get_agent_gateways(username: str, db: Session = Depends(get_db)):
    gateways = db.query(AgentGateway).filter(AgentGateway.username == username).all()
    result = []
    for g in gateways:
        result.append({
            "id": g.id,
            "region": g.region,
            "type": g.type,
            "name": g.name,
            "details": g.details,
            "min": g.min,
            "max": g.max,
            "badge": g.badge,
            "active": g.active
        })
    return result

@app.post("/api/agent/gateways")
def save_agent_gateway(data: GatewaySchema, db: Session = Depends(get_db)):
    new_gw = AgentGateway(
        username=data.username,
        region=data.region,
        type=data.type,
        name=data.name,
        details=data.details,
        min=data.min,
        max=data.max,
        badge=data.badge,
        active=data.active if data.active is not None else True
    )
    db.add(new_gw)
    db.commit()
    db.refresh(new_gw)
    return {"status": "success", "message": "Gateway saved successfully", "id": new_gw.id}

@app.post("/api/admin/login")
def admin_login(data: AdminLoginSchema, db: Session = Depends(get_db)):
    admin_pwd_setting = db.query(SystemSetting).filter(SystemSetting.key == "admin_password").first()
    correct_password = admin_pwd_setting.value if admin_pwd_setting else "admin123"
    
    if data.password == correct_password:
        return {"status": "success", "message": "Admin login successful"}
    else:
        raise HTTPException(status_code=401, detail="Incorrect admin password")

@app.post("/api/admin/change-password")
def admin_change_password(data: AdminChangePasswordSchema, db: Session = Depends(get_db)):
    admin_pwd_setting = db.query(SystemSetting).filter(SystemSetting.key == "admin_password").first()
    current_correct = admin_pwd_setting.value if admin_pwd_setting else "admin123"
    
    if data.current_password != current_correct:
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    if not admin_pwd_setting:
        admin_pwd_setting = SystemSetting(key="admin_password", value=data.new_password)
        db.add(admin_pwd_setting)
    else:
        admin_pwd_setting.value = data.new_password
        
    db.commit()
    return {"status": "success", "message": "Admin password updated successfully"}

@app.get("/api/support-settings")
def get_support_settings(db: Session = Depends(get_db)):
    tg = db.query(SystemSetting).filter(SystemSetting.key == "telegram_link").first()
    email = db.query(SystemSetting).filter(SystemSetting.key == "support_email").first()
    return {
        "telegram_link": tg.value if tg else "https://t.me/PayGaidSupport",
        "support_email": email.value if email else "support@paygaid.com"
    }

@app.post("/api/admin/support-settings/update")
def update_support_settings(data: SupportSettingsSchema, db: Session = Depends(get_db)):
    tg = db.query(SystemSetting).filter(SystemSetting.key == "telegram_link").first()
    if not tg:
        tg = SystemSetting(key="telegram_link", value=data.telegram_link)
        db.add(tg)
    else:
        tg.value = data.telegram_link

    email = db.query(SystemSetting).filter(SystemSetting.key == "support_email").first()
    if not email:
        email = SystemSetting(key="support_email", value=data.support_email)
        db.add(email)
    else:
        email.value = data.support_email

    db.commit()
    return {"status": "success", "message": "Support settings updated successfully"}

@app.post("/api/contact")
def submit_contact_message(data: ContactMessageSchema, db: Session = Depends(get_db)):
    new_msg = ContactSupportMessage(
        name=data.name,
        email=data.email,
        phone=data.phone,
        subject=data.subject,
        message=data.message,
        status="Pending",
        created_at=get_local_time("Bangladesh")
    )
    db.add(new_msg)
    db.commit()
    return {"status": "success", "message": "Support message sent successfully!"}

@app.get("/api/admin/contacts")
def get_admin_contact_messages(db: Session = Depends(get_db)):
    messages = db.query(ContactSupportMessage).order_by(ContactSupportMessage.id.desc()).all()
    result = []
    for msg in messages:
        result.append({
            "id": msg.id,
            "name": msg.name,
            "email": msg.email,
            "phone": msg.phone,
            "subject": msg.subject,
            "message": msg.message,
            "status": msg.status,
            "created_at": msg.created_at.strftime("%d %b %Y, %I:%M %p") if msg.created_at else ""
        })
    return result

@app.post("/api/admin/contacts/{contact_id}/resolve")
def resolve_contact_message(contact_id: int, db: Session = Depends(get_db)):
    msg = db.query(ContactSupportMessage).filter(ContactSupportMessage.id == contact_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Contact message not found")
    msg.status = "Resolved"
    db.commit()
    return {"status": "success", "message": "Contact marked as resolved."}

@app.get("/api/crypto/gateways")
def get_crypto_gateways(db: Session = Depends(get_db)):
    gateways = db.query(models.CryptoGateway).all()
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=tron,tether,litecoin,bitcoin&vs_currencies=bdt"
        response = requests.get(url, timeout=5)
        prices = response.json()
        
        trx_bdt = float(prices.get("tron", {}).get("bdt", 12.0))
        usdt_bdt = float(prices.get("tether", {}).get("bdt", 120.0)) + 3.0
        ltc_bdt = float(prices.get("litecoin", {}).get("bdt", 11000.0)) + 3.0
        btc_bdt = float(prices.get("bitcoin", {}).get("bdt", 8500000.0)) + 3.0
    except Exception:
        trx_bdt = 12.0
        usdt_bdt = 125.0
        ltc_bdt = 11423.0
        btc_bdt = 8500003.0

    result = []
    for gw in gateways:
        rate_str = gw.exchange_rate
        if gw.symbol == "TRON":
            rate_str = f"1 TRX = {trx_bdt:.2f} BDT"
        elif "USDT" in gw.symbol:
            rate_str = f"1 USDT = {usdt_bdt:.2f} BDT"
        elif gw.symbol == "LTC":
            rate_str = f"1 LTC = {ltc_bdt:.2f} BDT"
        elif gw.symbol == "BTC":
            rate_str = f"1 BTC = {btc_bdt:.2f} BDT"

        fixed_icon_html = gw.icon_html
        if "style=" not in fixed_icon_html:
            fixed_icon_html = fixed_icon_html.replace("<img ", "<img style='width:24px;height:24px;object-fit:contain;display:inline-block;' ")
        else:
            fixed_icon_html = fixed_icon_html.replace("style='", "style='width:24px;height:24px;object-fit:contain;display:inline-block;")

        result.append({
            "id": gw.id,
            "symbol": gw.symbol,
            "name": gw.name,
            "wallet_address": gw.wallet_address,
            "min_deposit": gw.min_deposit,
            "exchange_rate": rate_str,
            "icon_html": fixed_icon_html,
            "unique_code": gw.unique_code
        })
    return result

@app.post("/api/crypto/gateway/update")
def update_crypto_gateway(data: CryptoGatewayUpdateSchema, db: Session = Depends(get_db)):
    gw = db.query(models.CryptoGateway).filter(models.CryptoGateway.symbol == data.symbol).first()
    if not gw:
        raise HTTPException(status_code=404, detail="Gateway not found")
    gw.wallet_address = data.wallet_address
    gw.min_deposit = data.min_deposit
    db.commit()
    return {"status": "success", "message": "Gateway updated successfully"}

@app.get("/api/managers", response_model=List[ManagerSchema])
def get_verified_managers():
    return verified_managers_db

@app.post("/api/agents/register", status_code=status.HTTP_201_CREATED)
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

    if telegram:
        msg_text = (
            f"<b>PayGaid Agent Application Received!</b>\n\n"
            f"Hello <b>{full_name}</b>,\n"
            f"Your application has been submitted successfully.\n\n"
            f"🔑 <b>Application ID:</b> <code>{app_id}</code>\n\n"
            f"Please save this Application ID to check your application status later."
        )
        try:
            clean_target = telegram.strip().replace("@", "")
            chat_id = clean_target if (clean_target.isdigit() or clean_target.startswith("-")) else f"@{clean_target}"
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": msg_text, "parse_mode": "HTML"},
                timeout=5
            )
        except Exception as e:
            print("Telegram Notify Error:", e)

    return new_agent

@app.post("/api/agents/login")
async def agent_login(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
    except Exception:
        try:
            form = await request.form()
            data = dict(form)
        except Exception:
            data = {}

    identifier = (
        data.get("agent_username") or 
        data.get("username") or 
        data.get("agent_id") or 
        data.get("agentId") or 
        data.get("email") or 
        data.get("identifier") or 
        data.get("user") or 
        data.get("login")
    )
    password = (
        data.get("agent_password") or 
        data.get("password") or 
        data.get("pass") or 
        data.get("pwd") or 
        data.get("passWord")
    )
    
    if not identifier or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    agent = db.query(models.Agent).filter(
        (models.Agent.agent_username == identifier) | 
        (models.Agent.email == identifier) | 
        (models.Agent.application_id == identifier)
    ).first()
    
    if not agent or agent.agent_password != password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
        
    if agent.status and agent.status.lower() in ["deactivated", "inactive", "suspended", "rejected"]:
        raise HTTPException(status_code=400, detail="Your account is deactivated. Please contact support.")
        
    currency_sym = COUNTRY_CURRENCY_MAP.get(agent.country, getattr(agent, "currency_symbol", "RM"))
    
    return {
        "status": "success",
        "message": "Login successful",
        "agent_id": agent.agent_username or agent.application_id,
        "full_name": agent.full_name or agent.agent_username or "Agent",
        "currency_symbol": currency_sym
    }

@app.post("/api/agents/forgot-password")
def forgot_password_otp(data: ForgotPasswordRequestSchema, db: Session = Depends(get_db)):
    target_val = data.target.strip()
    if not target_val:
        raise HTTPException(status_code=400, detail="Email or Telegram username is required.")

    if data.method == "email":
        agent = db.query(models.Agent).filter(models.Agent.email == target_val).first()
    else:
        clean_tg = target_val.replace("@", "")
        agent = db.query(models.Agent).filter(
            (models.Agent.agent_username == target_val) | 
            (models.Agent.agent_username == clean_tg) | 
            (models.Agent.telegram == target_val) | 
            (models.Agent.telegram == clean_tg)
        ).first()

    if not agent:
        raise HTTPException(status_code=404, detail="No agent account found with this information.")

    otp_code = "".join(random.choices(string.digits, k=6))

    otp_record = models.PasswordResetOTP(
        agent_id=agent.agent_username or agent.application_id,
        method=data.method,
        target=target_val,
        otp_code=otp_code,
        is_used=False
    )
    db.add(otp_record)
    db.commit()

    return {
        "status": "success", 
        "message": f"Verification code generated successfully! (Your OTP is: {otp_code})"
    }

@app.post("/api/agents/reset-password-otp")
def reset_password_with_otp(data: ResetPasswordWithOTPSchema, db: Session = Depends(get_db)):
    target_val = data.target.strip()
    otp_val = data.otp_code.strip()
    new_pwd = data.new_password.strip()

    if not target_val or not otp_val or not new_pwd:
        raise HTTPException(status_code=400, detail="All fields are required.")

    otp_entry = db.query(models.PasswordResetOTP).filter(
        (models.PasswordResetOTP.target == target_val),
        (models.PasswordResetOTP.otp_code == otp_val),
        (models.PasswordResetOTP.is_used == False)
    ).order_by(models.PasswordResetOTP.id.desc()).first()

    if not otp_entry:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP code.")

    agent = db.query(models.Agent).filter(
        (models.Agent.agent_username == otp_entry.agent_id) | 
        (models.Agent.application_id == otp_entry.agent_id) | 
        (models.Agent.email == target_val)
    ).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent account not found.")

    agent.agent_password = new_pwd
    otp_entry.is_used = True
    db.commit()

    return {"status": "success", "message": "Password reset successfully! You can now log in."}

@app.post("/api/agent/change-password")
async def change_agent_password(data: ChangePasswordSchema, db: Session = Depends(get_db)):
    identifier = data.username or data.agent_id
    if not identifier:
        raise HTTPException(status_code=400, detail="Agent identifier is required")

    agent = db.query(models.Agent).filter(
        (models.Agent.agent_username == identifier) | 
        (models.Agent.application_id == identifier) |
        (models.Agent.email == identifier)
    ).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if agent.agent_password != data.current_password:
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    agent.agent_password = data.new_password
    db.commit()
    return {"status": "success", "message": "Password updated successfully"}

@app.get("/api/agent/profile/{agent_identifier}")
@app.get("/api/agents/profile/{agent_identifier}")
def get_agent_profile(agent_identifier: str, db: Session = Depends(get_db)):
    agent = db.query(models.Agent).filter(
        (models.Agent.agent_username == agent_identifier) | 
        (models.Agent.email == agent_identifier) | 
        (models.Agent.application_id == agent_identifier)
    ).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent profile not found")
        
    if agent.status and agent.status.lower() in ["deactivated", "inactive", "suspended", "rejected"]:
        raise HTTPException(status_code=400, detail="Account is deactivated")
        
    resolved_name = agent.full_name if (agent.full_name and agent.full_name.strip() != "") else (agent.agent_username or "Agent User")
    phone = agent.mobile or agent.whatsapp or "N/A"
    email_val = agent.email or "N/A"
    
    manager_tg = getattr(agent, "telegram", None) or getattr(agent, "assigned_manager", None) or ""

    bal = 0.0
    for col in ["opening_balance", "balance"]:
        if hasattr(agent, col) and getattr(agent, col) is not None:
            try:
                bal = float(getattr(agent, col))
                break
            except:
                pass

    currency_sym = COUNTRY_CURRENCY_MAP.get(agent.country, getattr(agent, "currency_symbol", "RM"))

    return {
        "status": "success",
        "agent_id": agent.agent_username or agent.application_id,
        "username": agent.agent_username or agent.application_id,
        "full_name": resolved_name,
        "fullName": resolved_name,
        "name": resolved_name,
        "agent_name": resolved_name,
        "agentName": resolved_name,
        "email": email_val,
        "email_address": email_val,
        "mobile": phone,
        "phone": phone,
        "phone_number": phone,
        "whatsapp": agent.whatsapp,
        "telegram": manager_tg,
        "assigned_manager": manager_tg,
        "balance": bal,
        "total_commission": agent.total_commission or 0.0,
        "today_commission": agent.today_commission or 0.0,
        "status": agent.status,
        "country": agent.country or "Malaysia",
        "currency_symbol": currency_sym,
        "registration_date": agent.created_at.strftime("%d %b, %Y") if hasattr(agent, "created_at") and agent.created_at else "09 Oct, 2026",
        "payment_gateway": agent.payment_gateway,
        "account_number": agent.account_number
    }

class CreateDepositRequestSchema(BaseModel):
    agent_id: str
    amount: float
    commission_rate: float
    method: str
    serial_id: str
    transaction_id: str

@app.post("/api/admin/deposit-request")
def create_deposit_request_admin(data: CreateDepositRequestSchema, db: Session = Depends(get_db)):
    agent = db.query(models.Agent).filter(
        (models.Agent.agent_username == data.agent_id) | 
        (models.Agent.application_id == data.agent_id)
    ).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    comm_amount = (data.amount * data.commission_rate) / 100.0
    save_agent_id = agent.agent_username if agent.agent_username else agent.application_id

    new_req = models.DepositRequest(
        serial_id=data.serial_id,
        agent_id=save_agent_id,
        amount=data.amount,
        commission_rate=data.commission_rate,
        commission_amount=comm_amount,
        transaction_id=data.transaction_id,
        method=data.method,
        status="Pending",
        created_at=get_local_time(agent.country)
    )
    db.add(new_req)
    db.commit()
    return {"status": "success", "message": "Deposit request sent successfully"}

@app.get("/api/admin/deposit-requests")
def get_admin_deposit_requests(db: Session = Depends(get_db)):
    requests_list = db.query(models.DepositRequest).order_by(models.DepositRequest.id.desc()).all()
    result = []
    for req in requests_list:
        agent = db.query(models.Agent).filter(
            (models.Agent.agent_username == req.agent_id) | 
            (models.Agent.application_id == req.agent_id)
        ).first()
        agent_name = agent.full_name if agent else req.agent_id
        currency_sym = get_agent_currency(db, req.agent_id)

        result.append({
            "id": req.id,
            "serialId": req.serial_id,
            "agentId": req.agent_id,
            "agentName": agent_name,
            "amount": req.amount,
            "commission_rate": req.commission_rate,
            "commission": req.commission_amount,
            "currency_symbol": currency_sym,
            "txId": req.transaction_id,
            "method": req.method,
            "status": req.status.lower(),
            "date": req.created_at.strftime("%d %b %Y") if req.created_at else "",
            "time": req.created_at.strftime("%I:%M %p") if req.created_at else ""
        })
    return result

@app.get("/api/agent/deposit-requests/{agent_id}")
def get_agent_deposit_requests(agent_id: str, db: Session = Depends(get_db)):
    if not agent_id or agent_id == "undefined" or agent_id == "null":
        return []

    agent = db.query(models.Agent).filter(
        (models.Agent.agent_username == agent_id) | 
        (models.Agent.application_id == agent_id) |
        (models.Agent.email == agent_id)
    ).first()

    target_ids = [agent_id]
    if agent:
        if agent.agent_username:
            target_ids.append(agent.agent_username)
        if agent.application_id:
            target_ids.append(agent.application_id)

    requests_list = db.query(models.DepositRequest).filter(
        models.DepositRequest.agent_id.in_(target_ids)
    ).order_by(models.DepositRequest.id.desc()).all()
    
    currency_sym = get_agent_currency(db, agent_id)
    result = []
    for req in requests_list:
        result.append({
            "id": req.id,
            "serialId": req.serial_id,
            "amount": req.amount,
            "commission_rate": req.commission_rate,
            "commission": req.commission_amount,
            "currency_symbol": currency_sym,
            "txId": req.transaction_id,
            "method": req.method,
            "status": req.status.lower(),
            "date": req.created_at.strftime("%d %b %Y") if req.created_at else "",
            "time": req.created_at.strftime("%I:%M %p") if req.created_at else ""
        })
    return result

@app.post("/api/agent/deposit-requests/{request_id}/action")
async def action_deposit_request(request_id: int, request: Request, db: Session = Depends(get_db)):
    try: data = await request.json()
    except: data = {}
    
    action = data.get("action")
    dep_req = db.query(models.DepositRequest).filter(models.DepositRequest.id == request_id).first()
    if not dep_req:
        raise HTTPException(status_code=404, detail="Deposit request not found")
        
    if dep_req.status != "Pending":
        raise HTTPException(status_code=400, detail="Request already processed")

    if action == "approve":
        dep_req.status = "Approved"
        agent = db.query(models.Agent).filter(
            (models.Agent.agent_username == dep_req.agent_id) | 
            (models.Agent.application_id == dep_req.agent_id)
        ).first()
        
        if agent:
            current_balance = 0.0
            for col in ["opening_balance", "balance"]:
                if hasattr(agent, col) and getattr(agent, col) is not None:
                    try:
                        current_balance = float(getattr(agent, col))
                        break
                    except:
                        pass
            
            new_balance = current_balance - dep_req.amount + (dep_req.commission_amount or 0.0)
            for col in ["opening_balance", "balance"]:
                if hasattr(agent, col):
                    setattr(agent, col, new_balance)

            agent.total_commission = (agent.total_commission or 0.0) + dep_req.commission_amount
            agent.today_commission = (agent.today_commission or 0.0) + dep_req.commission_amount
            
    elif action == "reject":
        dep_req.status = "Rejected"
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    db.commit()
    return {"status": "success", "message": f"Request {action}d successfully"}

@app.post("/api/admin/withdrawal-request")
def create_withdrawal_request_admin(data: CreateWithdrawRequestSchema, db: Session = Depends(get_db)):
    agent = db.query(models.Agent).filter(
        (models.Agent.agent_username == data.agent_id) | 
        (models.Agent.application_id == data.agent_id)
    ).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    comm_amount = (data.amount * data.commission_rate) / 100.0
    save_agent_id = agent.agent_username if agent.agent_username else agent.application_id

    new_wd = Withdrawal(
        agent_id=save_agent_id,
        full_name=agent.full_name or "Agent",
        method=data.method,
        amount=data.amount,
        commission_rate=data.commission_rate,
        commission_amount=comm_amount,
        wallet_address=data.wallet_address,
        status="Pending",
        assigned_agent_id=save_agent_id,
        request_type="user_withdrawal",
        created_at=get_local_time(agent.country)
    )
    db.add(new_wd)
    db.commit()
    return {"status": "success", "message": "Withdrawal request sent successfully"}

@app.get("/api/agent/withdrawal-requests/{agent_id}")
def get_agent_withdrawal_requests(agent_id: str, db: Session = Depends(get_db)):
    if not agent_id or agent_id == "undefined" or agent_id == "null":
        return []

    agent = db.query(models.Agent).filter(
        (models.Agent.agent_username == agent_id) | 
        (models.Agent.application_id == agent_id) |
        (models.Agent.email == agent_id)
    ).first()

    target_ids = [agent_id]
    if agent:
        if agent.agent_username:
            target_ids.append(agent.agent_username)
        if agent.application_id:
            target_ids.append(agent.application_id)

    requests_list = db.query(Withdrawal).filter(
        Withdrawal.assigned_agent_id.in_(target_ids),
        Withdrawal.request_type == "user_withdrawal"
    ).order_by(Withdrawal.id.desc()).all()
    
    currency_sym = get_agent_currency(db, agent_id)

    result = []
    for req in requests_list:
        result.append({
            "id": req.id,
            "serialId": f"#WD-{req.id}",
            "amount": req.amount,
            "commission_rate": getattr(req, "commission_rate", 0.0),
            "commission": getattr(req, "commission_amount", 0.0),
            "currency_symbol": currency_sym,
            "account": req.wallet_address,
            "method": req.method,
            "status": req.status.lower(),
            "date": req.created_at.strftime("%d %b %Y") if req.created_at else "",
            "time": req.created_at.strftime("%I:%M %p") if req.created_at else "",
            "reason": req.rejection_reason or ""
        })
    return result

@app.get("/api/agent/recent-activities/{agent_id}")
def get_agent_recent_activities(agent_id: str, db: Session = Depends(get_db)):
    activities = []
    currency_sym = get_agent_currency(db, agent_id)
    
    if not agent_id or agent_id == "undefined" or agent_id == "null":
        return []

    agent = db.query(models.Agent).filter(
        (models.Agent.agent_username == agent_id) | 
        (models.Agent.application_id == agent_id) |
        (models.Agent.email == agent_id)
    ).first()
    
    target_ids = [agent_id]
    if agent:
        if agent.agent_username:
            target_ids.append(agent.agent_username)
        if agent.application_id:
            target_ids.append(agent.application_id)

    deposits = db.query(models.DepositRequest).filter(
        models.DepositRequest.agent_id.in_(target_ids)
    ).all()

    withdrawals = db.query(Withdrawal).filter(
        or_(
            Withdrawal.agent_id.in_(target_ids),
            Withdrawal.assigned_agent_id.in_(target_ids)
        )
    ).all()

    for dep in deposits:
        status_text = dep.status.capitalize() if dep.status else "Pending"
        activities.append({
            "type": "deposit",
            "title": f"{dep.method.upper()} Deposit {status_text}",
            "subtitle": f"Serial: {dep.serial_id} | TrxID: {dep.transaction_id}",
            "amount": dep.amount,
            "currency_symbol": currency_sym,
            "commission": dep.commission_amount or 0.0,
            "status": dep.status.lower() if dep.status else "pending",
            "created_at": dep.created_at.isoformat() if dep.created_at else get_local_time().isoformat()
        })
        if dep.commission_amount and dep.commission_amount > 0 and dep.status and dep.status.lower() == "approved":
            activities.append({
                "type": "commission",
                "title": "Commission Earned",
                "subtitle": f"From {dep.method.upper()} Trx #{dep.transaction_id}",
                "amount": dep.commission_amount,
                "currency_symbol": currency_sym,
                "commission": dep.commission_amount,
                "status": "approved",
                "created_at": dep.created_at.isoformat() if dep.created_at else get_local_time().isoformat()
            })

    for wd in withdrawals:
        status_text = wd.status.capitalize() if wd.status else "Pending"
        req_type = getattr(wd, "request_type", "")
        
        if req_type == "user_withdrawal" or wd.assigned_agent_id in target_ids:
            title_prefix = f"{wd.method.upper()} Withdraw Request {status_text}"
            activities.append({
                "type": "user_withdraw",
                "title": title_prefix,
                "subtitle": f"Account: {wd.wallet_address}",
                "amount": wd.amount,
                "currency_symbol": currency_sym,
                "commission": wd.commission_amount or 0.0,
                "status": wd.status.lower() if wd.status else "pending",
                "created_at": wd.created_at.isoformat() if wd.created_at else get_local_time().isoformat(),
                "reason": wd.rejection_reason or ""
            })
            if wd.commission_amount and wd.commission_amount > 0 and wd.status and wd.status.lower() == "approved":
                activities.append({
                    "type": "commission",
                    "title": "Commission Earned",
                    "subtitle": f"From {wd.method.upper()} Withdrawal #{wd.id}",
                    "amount": wd.commission_amount,
                    "currency_symbol": currency_sym,
                    "commission": wd.commission_amount,
                    "status": "approved",
                    "created_at": wd.created_at.isoformat() if wd.created_at else get_local_time().isoformat()
                })
        else:
            activities.append({
                "type": "withdraw",
                "title": f"{wd.method.upper()} Main Balance Withdraw {status_text}",
                "subtitle": f"Account: {wd.wallet_address}",
                "amount": wd.amount,
                "currency_symbol": currency_sym,
                "commission": wd.commission_amount or 0.0,
                "status": wd.status.lower() if wd.status else "pending",
                "created_at": wd.created_at.isoformat() if wd.created_at else get_local_time().isoformat(),
                "reason": wd.rejection_reason or ""
            })

    activities.sort(key=lambda x: x["created_at"], reverse=True)
    return activities

@app.post("/api/agent/complain")
async def create_complain(request: Request, db: Session = Depends(get_db)):
    try: data = await request.json()
    except Exception: data = {}

    username = data.get("username") or data.get("agent_id")
    category = data.get("category")
    transaction_id = data.get("transaction_id", "N/A")
    description = data.get("description")

    if not username or not category or not description:
        raise HTTPException(status_code=400, detail="All required fields must be provided")

    agent = db.query(models.Agent).filter(
        (models.Agent.agent_username == username) | 
        (models.Agent.application_id == username)
    ).first()

    agent_name = agent.full_name if agent else username

    new_complain = models.Complain(
        agent_id=str(username),
        full_name=agent_name,
        category=category,
        transaction_id=transaction_id,
        description=description,
        status="Pending",
        created_at=get_local_time(agent.country if agent else "Bangladesh")
    )
    db.add(new_complain)
    db.commit()
    return {"status": "success", "message": "Complain submitted successfully"}

@app.get("/api/admin/complains")
def get_admin_complains(db: Session = Depends(get_db)):
    return db.query(models.Complain).order_by(models.Complain.id.desc()).all()

@app.post("/api/admin/complains/{complain_id}/approve")
def approve_complain(complain_id: int, db: Session = Depends(get_db)):
    complain = db.query(models.Complain).filter(models.Complain.id == complain_id).first()
    if not complain:
        raise HTTPException(status_code=404, detail="Complain not found")
    complain.status = "Approved"
    db.commit()
    return {"status": "success", "message": "Complain approved successfully"}

@app.post("/api/admin/complains/{complain_id}/reject")
async def reject_complain(complain_id: int, request: Request, db: Session = Depends(get_db)):
    try: data = await request.json()
    except Exception: data = {}
    reason = data.get("reason", "Admin rejected the complain")

    complain = db.query(models.Complain).filter(models.Complain.id == complain_id).first()
    if not complain:
        raise HTTPException(status_code=404, detail="Complain not found")
    
    complain.status = "Rejected"
    complain.rejection_reason = reason
    db.commit()
    return {"status": "success", "message": "Complain rejected successfully"}

@app.post("/api/agent/withdraw")
async def create_withdrawal(request: Request, db: Session = Depends(get_db)):
    try: data = await request.json()
    except Exception: data = {}

    username = data.get("username") or data.get("agent_id")
    method = data.get("method")
    amount = data.get("amount")
    wallet_address = data.get("wallet_address")

    if not username or not method or not amount or not wallet_address:
        raise HTTPException(status_code=400, detail="All fields are required")

    agent = db.query(models.Agent).filter(
        (models.Agent.agent_username == username) | 
        (models.Agent.application_id == username)
    ).first()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    wd_amount = float(amount)

    current_balance = 0.0
    for col in ["opening_balance", "balance"]:
        if hasattr(agent, col) and getattr(agent, col) is not None:
            try:
                current_balance = float(getattr(agent, col))
                break
            except:
                pass

    if current_balance < wd_amount:
        raise HTTPException(status_code=400, detail="Insufficient main balance for withdrawal")

    new_balance = current_balance - wd_amount
    for col in ["opening_balance", "balance"]:
        if hasattr(agent, col):
            setattr(agent, col, new_balance)

    new_withdrawal = Withdrawal(
        agent_id=agent.agent_username or agent.application_id,
        full_name=agent.full_name or "Agent",
        method=method,
        amount=wd_amount,
        commission_rate=0.0,
        commission_amount=0.0,
        wallet_address=wallet_address,
        status="Pending",
        request_type="agent_withdrawal",
        created_at=get_local_time(agent.country)
    )

    db.add(new_withdrawal)
    db.commit()

    return {"status": "success", "message": "Withdrawal request submitted successfully"}

@app.get("/api/admin/withdrawals")
def get_admin_withdrawals(db: Session = Depends(get_db)):
    return db.query(Withdrawal).order_by(Withdrawal.id.desc()).all()

@app.post("/api/admin/withdrawals/{withdraw_id}/approve")
def approve_withdrawal(withdraw_id: int, db: Session = Depends(get_db)):
    wd = db.query(Withdrawal).filter(Withdrawal.id == withdraw_id).first()
    if not wd:
        raise HTTPException(status_code=404, detail="Withdrawal request not found")
    
    if wd.status == "Approved":
        return {"message": "Already approved"}

    wd.status = "Approved"

    if getattr(wd, "request_type", "") == "user_withdrawal" or wd.assigned_agent_id:
        target_agent_id = wd.assigned_agent_id or wd.agent_id
        agent = db.query(models.Agent).filter(
            (models.Agent.agent_username == target_agent_id) | 
            (models.Agent.application_id == target_agent_id)
        ).first()

        if agent:
            current_balance = 0.0
            for col in ["opening_balance", "balance"]:
                if hasattr(agent, col) and getattr(agent, col) is not None:
                    try:
                        current_balance = float(getattr(agent, col))
                        break
                    except:
                        pass
            
            comm_amount = wd.commission_amount or 0.0
            new_balance = current_balance + wd.amount + comm_amount

            for col in ["opening_balance", "balance"]:
                if hasattr(agent, col):
                    setattr(agent, col, new_balance)

            agent.total_commission = (agent.total_commission or 0.0) + comm_amount
            agent.today_commission = (agent.today_commission or 0.0) + comm_amount

    db.commit()
    return {"status": "success", "message": "Withdrawal approved and balance/commission updated successfully"}

@app.post("/api/admin/withdrawals/{withdraw_id}/reject")
async def reject_withdrawal(withdraw_id: int, request: Request, db: Session = Depends(get_db)):
    try: data = await request.json()
    except Exception: data = {}
    reason = data.get("reason", "Admin rejected the request")

    wd = db.query(Withdrawal).filter(Withdrawal.id == withdraw_id).first()
    if not wd:
        raise HTTPException(status_code=404, detail="Withdrawal request not found")
    
    if wd.status == "Rejected":
        return {"message": "Already rejected"}

    wd.status = "Rejected"
    wd.rejection_reason = reason

    agent = db.query(models.Agent).filter(
        (models.Agent.agent_username == wd.agent_id) | 
        (models.Agent.application_id == wd.agent_id)
    ).first()

    if agent and (getattr(wd, "request_type", "") == "agent_withdrawal" or not wd.assigned_agent_id):
        cur_bal = 0.0
        for col in ["opening_balance", "balance"]:
            if hasattr(agent, col) and getattr(agent, col) is not None:
                try:
                    cur_bal = float(getattr(agent, col))
                    break
                except:
                    pass
        
        refund_balance = cur_bal + wd.amount
        for col in ["opening_balance", "balance"]:
            if hasattr(agent, col):
                setattr(agent, col, refund_balance)

    db.commit()
    return {"status": "success", "message": "Withdrawal rejected successfully"}

@app.get("/api/agents")
def get_all_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    agents = db.query(models.Agent).offset(skip).limit(limit).all()
    result = []
    for ag in agents:
        disp_id = ag.agent_username if (ag.agent_username and ag.agent_username.strip() != "") else ag.application_id
        
        current_bal = 0.0
        for col in ["opening_balance", "balance"]:
            if hasattr(ag, col) and getattr(ag, col) is not None:
                try:
                    val = float(getattr(ag, col))
                    current_bal = val
                    if val > 0:
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
            "status": ag.status,
            "language": ag.language
        })
    return result

@app.patch("/api/agents/{agent_id}/balance")
@app.post("/api/agents/{agent_id}/balance")
def update_agent_balance_admin(agent_id: int, data: BalanceUpdateSchema, db: Session = Depends(get_db)):
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    current_balance = 0.0
    for col in ["opening_balance", "balance"]:
        if hasattr(agent, col) and getattr(agent, col) is not None:
            try:
                current_balance = float(getattr(agent, col))
                break
            except:
                pass

    new_balance = current_balance + float(data.amount)
    
    updated = False
    for col in ["opening_balance", "balance"]:
        if hasattr(agent, col):
            setattr(agent, col, new_balance)
            updated = True

    if not updated:
        agent.opening_balance = new_balance

    db.commit()
    db.refresh(agent)
    return {"status": "success", "message": "Balance updated successfully", "new_balance": new_balance}

@app.patch("/api/agents/{agent_id}/status")
@app.post("/api/agents/{agent_id}/status")
@app.patch("/api/agents/{agent_id}")
@app.post("/api/agents/{agent_id}")
def update_agent_general_or_status(agent_id: int, update_data: AdminUpdatePayload, db: Session = Depends(get_db)):
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if update_data.status is not None:
        agent.status = update_data.status
    if update_data.assigned_manager is not None:
        agent.assigned_manager = update_data.assigned_manager
    if update_data.message is not None:
        agent.message = update_data.message
    if update_data.deposit_limit_status is not None:
        agent.deposit_limit_status = update_data.deposit_limit_status
    if update_data.withdrawal_limit_status is not None:
        agent.withdrawal_limit_status = update_data.withdrawal_limit_status
    if update_data.security_deposit_status is not None:
        agent.security_deposit_status = update_data.security_deposit_status
    if update_data.full_name is not None:
        agent.full_name = update_data.full_name
    if update_data.mobile is not None or update_data.phone_number is not None:
        agent.mobile = update_data.mobile or update_data.phone_number
    if update_data.email is not None or update_data.email_address is not None:
        agent.email = update_data.email or update_data.email_address
    if update_data.balance is not None:
        new_b = float(update_data.balance)
        for col in ["opening_balance", "balance"]:
            if hasattr(agent, col):
                setattr(agent, col, new_b)
    if update_data.password is not None and update_data.password.strip() != "":
        agent.agent_password = update_data.password

    db.commit()
    db.refresh(agent)
    return {"status": "success", "message": "Agent updated successfully"}

@app.delete("/api/agents/{agent_id}")
def delete_agent_admin(agent_id: int, db: Session = Depends(get_db)):
    agent = db.query(models.Agent).filter(models.Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    db.delete(agent)
    db.commit()
    return {"status": "success", "message": "Agent deleted successfully"}

@app.post("/api/agents-manual")
def register_manual_agent(data: ManualAgentRegisterRequest, db: Session = Depends(get_db)):
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Password and Confirm Password do not match.")

    existing_agent = db.query(models.Agent).filter(models.Agent.agent_username == data.agent_id).first()
    if existing_agent:
        raise HTTPException(status_code=400, detail="Agent ID / Username already exists.")

    init_bal = float(data.opening_balance)
    forced_currency = COUNTRY_CURRENCY_MAP.get(data.country, data.currency_symbol or "RM")

    new_agent = models.Agent(
        application_id=generate_application_id(),
        country=data.country,
        currency_symbol=forced_currency,
        language="Manual",
        full_name=data.full_name,
        email=data.email_address,
        mobile=data.phone_number,
        whatsapp="",
        telegram=data.manager_telegram or "",
        assigned_manager=data.manager_telegram or "",
        payment_gateway=data.wallet_name,
        account_number=data.wallet_account_number,
        doc_type="Manual",
        doc_number="N/A",
        front_image="N/A",
        back_image="N/A",
        agent_username=data.agent_id,
        agent_password=data.password,
        opening_balance=init_bal,
        status="Active",
        created_at=get_local_time(data.country)
    )
    if hasattr(new_agent, "balance"):
        new_agent.balance = init_bal

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return {
        "success": True,
        "message": f"Manual agent account created successfully for {data.country} with currency {forced_currency}!",
        "agent_id": data.agent_id
    }

@app.get("/admin.html")
def serve_admin():
    file_path = os.path.join(os.getcwd(), "admin.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="admin.html not found")

@app.get("/login.html")
def serve_login():
    file_path = os.path.join(os.getcwd(), "login.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="login.html not found")

@app.get("/agent-dashboard.html")
def serve_agent_dashboard():
    file_path = os.path.join(os.getcwd(), "agent-dashboard.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="agent-dashboard.html not found")

@app.get("/request.html")
@app.get("/request.htm")
def serve_request_page():
    for fname in ["request.html", "request.htm"]:
        fpath = os.path.join(os.getcwd(), fname)
        if os.path.exists(fpath):
            return FileResponse(fpath)
    raise HTTPException(status_code=404, detail="request.html not found")

@app.get("/deposit-requests.html")
def serve_deposit_requests():
    file_path = os.path.join(os.getcwd(), "deposit-requests.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="deposit-requests.html not found")

@app.get("/withdraw-requests.html")
@app.get("/withdrawals.html")
def serve_withdraw_requests():
    for fname in ["withdraw-requests.html", "withdrawals.html"]:
        fpath = os.path.join(os.getcwd(), fname)
        if os.path.exists(fpath):
            return FileResponse(fpath)
    raise HTTPException(status_code=404, detail="withdraw-requests.html not found")

@app.get("/withdraw.html")
@app.get("/withdraw")
def serve_withdraw_form():
    file_path = os.path.join(os.getcwd(), "withdraw.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="withdraw.html not found")

@app.get("/recent-activity.html")
def serve_recent_activity():
    file_path = os.path.join(os.getcwd(), "recent-activity.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    alt_path = os.path.join(os.getcwd(), "transaction.html")
    if os.path.exists(alt_path):
        return FileResponse(alt_path)
    raise HTTPException(status_code=404, detail="recent-activity.html not found")

@app.get("/profile.html")
def serve_profile():
    file_path = os.path.join(os.getcwd(), "profile.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    alt_path = os.path.join(os.getcwd(), "agent-dashboard.html")
    if os.path.exists(alt_path):
        return FileResponse(alt_path)
    raise HTTPException(status_code=404, detail="profile.html not found")

@app.get("/transaction.html")
def serve_transaction():
    file_path = os.path.join(os.getcwd(), "transaction.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    alt_path = os.path.join(os.getcwd(), "agent-dashboard.html")
    if os.path.exists(alt_path):
        return FileResponse(alt_path)
    raise HTTPException(status_code=404, detail="transaction.html not found")

@app.get("/reports.html")
def serve_reports():
    file_path = os.path.join(os.getcwd(), "reports.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    alt_path = os.path.join(os.getcwd(), "agent-dashboard.html")
    if os.path.exists(alt_path):
        return FileResponse(alt_path)
    raise HTTPException(status_code=404, detail="reports.html not found")

@app.get("/complain.html")
@app.get("/contact-support.html")
@app.get("/support.html")
def serve_complain():
    for fname in ["complain.html", "contact-support.html", "support.html"]:
        fpath = os.path.join(os.getcwd(), fname)
        if os.path.exists(fpath):
            return FileResponse(fpath)
    alt_path = os.path.join(os.getcwd(), "agent-dashboard.html")
    if os.path.exists(alt_path):
        return FileResponse(alt_path)
    raise HTTPException(status_code=404, detail="complain.html not found")

@app.get("/gateways.html")
def serve_gateways():
    file_path = os.path.join(os.getcwd(), "gateways.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    alt_path = os.path.join(os.getcwd(), "agent-dashboard.html")
    if os.path.exists(alt_path):
        return FileResponse(alt_path)
    raise HTTPException(status_code=404, detail="gateways.html not found")

@app.get("/security.html")
def serve_security():
    file_path = os.path.join(os.getcwd(), "security.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    alt_path = os.path.join(os.getcwd(), "agent-dashboard.html")
    if os.path.exists(alt_path):
        return FileResponse(alt_path)
    raise HTTPException(status_code=404, detail="security.html not found")

@app.get("/accounts-manager.html")
def serve_accounts_manager():
    file_path = os.path.join(os.getcwd(), "accounts-manager.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    alt_path = os.path.join(os.getcwd(), "agent-dashboard.html")
    if os.path.exists(alt_path):
        return FileResponse(alt_path)
    raise HTTPException(status_code=404, detail="accounts-manager.html not found")

@app.get("/change-password.html")
def serve_change_password():
    file_path = os.path.join(os.getcwd(), "change-password.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    alt_path = os.path.join(os.getcwd(), "agent-dashboard.html")
    if os.path.exists(alt_path):
        return FileResponse(alt_path)
    raise HTTPException(status_code=404, detail="change-password.html not found")

@app.get("/forgot-password.html")
@app.get("/forgot-password")
def serve_forgot_password():
    file_path = os.path.join(os.getcwd(), "forgot-password.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="forgot-password.html not found")

@app.get("/add-money.html")
def serve_add_money():
    file_path = os.path.join(os.getcwd(), "add-money.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    alt_path = os.path.join(os.getcwd(), "agent-dashboard.html")
    if os.path.exists(alt_path):
        return FileResponse(alt_path)
    raise HTTPException(status_code=404, detail="add-money.html not found")

@app.get("/")
def serve_root():
    file_path = os.path.join(os.getcwd(), "index.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"message": "Portal API is running successfully"}

@app.get("/{file_name:path}")
def catch_all_html_files(file_name: str):
    if file_name.startswith("api/"):
        raise HTTPException(status_code=404, detail="API route not found")
        
    word_file = file_name if file_name.endswith(".html") else f"{file_name}.html"
    file_path = os.path.join(os.getcwd(), word_file)
    
    if os.path.exists(file_path):
        return FileResponse(file_path)
        
    alt_path = os.path.join(os.getcwd(), "index.html")
    if os.path.exists(alt_path):
        return FileResponse(alt_path)
        
    raise HTTPException(status_code=404, detail="Page not found")