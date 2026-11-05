import re

path = "/var/www/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# নিশ্চিত করা হচ্ছে যাতে get_all_agents রাউটটি সব পেন্ডিং ও নতুন আবেদন সঠিকভাবে ফেচ করে
new_get_agents = '''
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
'''

if 'def get_all_agents' in code:
    code = re.sub(r'@app\.get\("/api/agents"\)\s*def get_all_agents\(.*?(?=\n@app|\Z)', new_get_agents.strip(), code, flags=re.DOTALL)
else:
    code += "\n\n" + new_get_agents

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Admin panel agent sync fixed successfully!")
