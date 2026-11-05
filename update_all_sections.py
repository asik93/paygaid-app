import os
import re

file_path = "/var/www/app/index.html"
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # ১. Program Overview Professional Format
    new_overview = """PayGaid is a specialized high-risk payment gateway with elite expertise in iGaming and international high-risk financial transaction processing.<br><br>
As an official PayGaid Agent, you play a crucial role in facilitating seamless global transactions, onboarding verified partners, and bridging financial operations securely. Our platform provides robust infrastructure, transparent commission structures, and dedicated support to ensure sustainable business growth."""

    # ২. Eligibility Criteria Professional Format
    new_eligibility = """To qualify as an official PayGaid Agent, applicants must meet the following criteria:<br><br>
<ul style="text-align: left; padding-left: 20px; margin: 0;">
  <li style="margin-bottom: 8px;"><b>Verified Information:</b> Provide complete, valid, and accurate personal and business credentials.</li>
  <li style="margin-bottom: 8px;"><b>Communication Channels:</b> Maintain a verified Telegram account and active channels for efficient client management.</li>
  <li style="margin-bottom: 8px;"><b>Industry Experience:</b> Background in digital marketing, agency operations, or high-risk payment solutions is preferred.</li>
  <li style="margin-bottom: 8px;"><b>Compliance & Security:</b> Strict adherence to platform security standards, data privacy, and operational guidelines.</li>
</ul>"""

    # ৩. Terms & Conditions Professional Format
    new_terms = """<ol style="text-align: left; padding-left: 20px; margin: 0;">
  <li style="margin-bottom: 10px;"><b>Data Accuracy:</b> All information submitted during agent registration and deposit/withdrawal requests must be completely authentic and accurate.</li>
  <li style="margin-bottom: 10px;"><b>Professional Conduct:</b> Agents must maintain high professional standards and strictly adhere to PayGaid operational and security protocols.</li>
  <li style="margin-bottom: 10px;"><b>Zero Tolerance for Fraud:</b> Any fraudulent activity, unauthorized access attempts, or compliance breaches will lead to immediate account termination.</li>
  <li style="margin-bottom: 10px;"><b>Policy Updates:</b> PayGaid reserves the right to modify program terms, commission frameworks, and policies to maintain platform integrity.</li>
</ol>"""

    # ৪. FAQ Professional Format
    new_faq = """<b>Q1: What is PayGaid?</b><br>
PayGaid is a specialized high-risk payment gateway engineered to handle secure, fast, and compliant financial transactions for high-growth sectors like iGaming and international commerce.<br><br>
<b>Q2: How do I become a PayGaid Agent?</b><br>
You can apply directly through our official Telegram bot, submit your verification details, and access your agent portal dashboard to begin operations.<br><br>
<b>Q3: How are deposits and withdrawals managed?</b><br>
All transactions are processed securely through automated request modules integrated directly into our platform dashboard and Telegram mini app.<br><br>
<b>Q4: Where can I get technical or operational support?</b><br>
You can reach our dedicated support team anytime via the communication options provided inside the portal or through our official channels."""

    # ফাইলের ভেতরে সংশ্লিষ্ট সেকশনগুলো টার্গেট করে প্রফেশনাল ফরম্যাট বসানো
    # (যদি আপনার ফাইলে সেকশনগুলোর নির্দিষ্ট আইডি বা ক্লাস থাকে, সে অনুযায়ী ট্যাগগুলো আপডেট করা হলো)
    
    # ওভারভিউ আপডেট
    content = re.sub(r'PayGaid is a specialized high-risk payment gateway.*?(?=<\/div>|<\/section>|</div>|$)', new_overview, content, flags=re.DOTALL)
    
    # এলিজিবিলিটি আপডেট
    content = re.sub(r'To qualify as an official PayGaid Agent.*?(?=<\/div>|<\/section>|</div>|$)', new_eligibility, content, flags=re.DOTALL)
    
    # টার্মস আপডেট
    content = re.sub(r'1\. All information submitted.*?(?=<\/div>|<\/section>|</div>|$)', new_terms, content, flags=re.DOTALL)
    
    # এফএকিউ আপডেট
    content = re.sub(r'What is PayGaid\?.*?(?=<\/div>|<\/section>|</div>|$)', new_faq, content, flags=re.DOTALL)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("All 4 sections updated successfully with professional international layout!")
else:
    print("index.html not found!")
