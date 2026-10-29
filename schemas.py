from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# 1. Schema for Agent Registration (Input from User Form)
class AgentCreate(BaseModel):
    country: str
    language: str
    full_name: str
    email: EmailStr
    mobile: str
    whatsapp: Optional[str] = None
    telegram: Optional[str] = None
    payment_gateway: str
    account_number: str
    doc_type: str
    doc_number: str
    front_image: Optional[str] = None
    back_image: Optional[str] = None

# 2. Schema for Admin Approval / Status Update
class AgentAdminUpdate(BaseModel):
    status: str  # e.g., "Active", "Rejected", "Under Review"
    assigned_manager: str
    message: Optional[str] = None
    deposit_limit_status: Optional[str] = "Pending"
    withdrawal_limit_status: Optional[str] = "Pending"
    security_deposit_status: Optional[str] = "Pending"

# 3. Schema for Agent Login Request
class AgentLogin(BaseModel):
    agent_username: str
    agent_password: str

# 4. Schema for Response / Output sent back to Frontend
class AgentResponse(BaseModel):
    id: int
    application_id: str
    country: str
    language: str
    full_name: str
    email: str
    mobile: str
    whatsapp: Optional[str] = None
    telegram: Optional[str] = None
    payment_gateway: str
    account_number: str
    doc_type: str
    doc_number: str
    front_image: Optional[str] = None
    back_image: Optional[str] = None
    status: str
    assigned_manager: Optional[str] = None
    message: Optional[str] = None
    deposit_limit_status: Optional[str] = "Pending"
    withdrawal_limit_status: Optional[str] = "Pending"
    security_deposit_status: Optional[str] = "Pending"
    agent_username: Optional[str] = None
    agent_password: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True