import re

path = "/var/www/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

new_route = '''
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

    disp_id = new_agent.agent_username if (new_agent.agent_username and new_agent.agent_username.strip() != "") else new_agent.application_id

    return {
        "status": "success",
        "message": "Application submitted successfully",
        "application_id": new_agent.application_id,
        "agent_id": disp_id,
        "full_name": new_agent.full_name
    }
'''

if '@app.post("/api/agents/register"' in code:
    code = re.sub(r'@app\.post\("/api/agents/register"[^)]*\)\s*async def register_agent\(.*?(?=\n@app|\Z)', new_route.strip(), code, flags=re.DOTALL)
else:
    code += "\n\n" + new_route.strip()

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Successfully updated register route!")
