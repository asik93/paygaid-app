from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from database import Base

class Agent(Base):
    __tablename__ = "agents"

    # Primary Identification
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    application_id = Column(String, unique=True, index=True, nullable=False)

    # Location & Language
    country = Column(String, nullable=False)
    currency_symbol = Column(String, default="৳")
    language = Column(String, nullable=False)

    # Personal Details
    full_name = Column(String, nullable=False)
    email = Column(String, index=True, nullable=False)  # unique constraint removed
    mobile = Column(String, nullable=False)
    whatsapp = Column(String, nullable=True)
    telegram = Column(String, nullable=True)

    # Payment Information
    payment_gateway = Column(String, nullable=False)
    account_number = Column(String, nullable=False)

    # Identity Documents
    doc_type = Column(String, nullable=False)
    doc_number = Column(String, nullable=False)
    front_image = Column(String, nullable=True)  # File path or URL
    back_image = Column(String, nullable=True)   # File path or URL

    # Admin Control & Account Credentials
    status = Column(String, default="Pending")         # Pending, Active, Rejected
    assigned_manager = Column(String, nullable=True)   # Manager name/ID assigned by admin
    message = Column(String, nullable=True)
    
    # New Limit Status Fields
    deposit_limit_status = Column(String, default="Pending")
    withdrawal_limit_status = Column(String, default="Pending")
    security_deposit_status = Column(String, default="Pending")

    opening_balance = Column(Float, default=0.0)                 # Added opening balance
    balance = Column(Float, default=0.0)                         # Added balance field
    total_commission = Column(Float, default=0.0)                # Total Commission
    today_commission = Column(Float, default=0.0)                # Today Commission
    agent_username = Column(String, unique=True, nullable=True)  # Generated on approval
    agent_password = Column(String, nullable=True)               # Generated on approval
    
    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)

# Crypto Gateway Model
class CryptoGateway(Base):
    __tablename__ = "crypto_gateways"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    wallet_address = Column(String, nullable=False)
    min_deposit = Column(String, nullable=False)
    exchange_rate = Column(String, nullable=False)
    icon_html = Column(String, nullable=False)
    unique_code = Column(String, nullable=False)

# Complain Model
class Complain(Base):
    __tablename__ = "complains"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(String, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    transaction_id = Column(String, nullable=True)
    description = Column(String, nullable=False)
    status = Column(String, default="Pending")  # Pending, Approved, Rejected
    rejection_reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Deposit Request Model
class DepositRequest(Base):
    __tablename__ = "deposit_requests"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    serial_id = Column(String, unique=True, index=True, nullable=False)
    agent_id = Column(String, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    commission_rate = Column(Float, default=0.0)
    commission_amount = Column(Float, default=0.0)
    transaction_id = Column(String, nullable=False)
    method = Column(String, default="System")
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)

# Password Reset OTP Model
class PasswordResetOTP(Base):
    __tablename__ = "password_reset_otps"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    agent_id = Column(String, index=True, nullable=False)
    method = Column(String, nullable=False)  # email, telegram
    target = Column(String, nullable=False)  # email address or telegram username
    otp_code = Column(String, nullable=False)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)