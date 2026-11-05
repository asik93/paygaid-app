import os

file_path = "/var/www/app/index.html"
if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # আন্তর্জাতিক মানের প্রফেশনাল ইউআই ডিজাইন এবং স্টাইলিং সহ সম্পূর্ণ কনটেন্ট
    pro_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PayGaid Agent Portal</title>
    <style>
        :root {
            --primary-color: #0052FF;
            --bg-color: #F8FAFC;
            --card-bg: #FFFFFF;
            --text-main: #1E293B;
            --text-muted: #64748B;
            --border-color: #E2E8F0;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 16px;
            line-height: 1.6;
        }
        .container {
            max-width: 600px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            margin-bottom: 24px;
        }
        .header h1 {
            font-size: 22px;
            font-weight: 700;
            color: var(--text-main);
            margin: 0 0 4px 0;
        }
        .header p {
            font-size: 14px;
            color: var(--text-muted);
            margin: 0;
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .card h3 {
            font-size: 18px;
            font-weight: 600;
            color: var(--primary-color);
            margin-top: 0;
            margin-bottom: 12px;
            border-bottom: 2px solid #F1F5F9;
            padding-bottom: 8px;
        }
        p, li {
            font-size: 14px;
            color: var(--text-main);
        }
        ul, ol {
            padding-left: 20px;
            margin: 8px 0;
        }
        li {
            margin-bottom: 8px;
        }
        .faq-item {
            margin-bottom: 16px;
        }
        .faq-item:last-child {
            margin-bottom: 0;
        }
        .faq-question {
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 4px;
        }
        .faq-answer {
            color: var(--text-muted);
            font-size: 13px;
        }
        .footer {
            text-align: center;
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 24px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>PayGaid Agent Portal</h1>
        <p>Secure High-Risk Financial Infrastructure</p>
    </div>

    <!-- 1. Program Overview -->
    <div class="card">
        <h3>Program Overview</h3>
        <p><b>PayGaid Agent Program Overview</b></p>
        <p>PayGaid is a specialized high-risk payment gateway with expertise in iGaming and international high-risk payment processing. As a PayGaid Agent, you play a vital role in facilitating seamless transactions, onboarding verified clients, and bridging financial operations securely across regions. Our program is designed to offer robust support, transparent commission structures, and reliable infrastructure to ensure smooth business growth for all active partners.</p>
    </div>

    <!-- 2. Eligibility Criteria -->
    <div class="card">
        <h3>Eligibility Criteria</h3>
        <p><b>To qualify as an official PayGaid Agent, applicants must meet the following criteria:</b></p>
        <ul>
            <li>Applicants should provide complete, valid, and accurate personal and business information.</li>
            <li>Must possess a verified Telegram account and active communication channels for client management.</li>
            <li>Experience in digital marketing, agency operations, or online payment processing is preferred.</li>
            <li>Commitment to maintaining security standards, privacy, and compliance with platform guidelines.</li>
        </ul>
    </div>

    <!-- 3. Terms & Conditions -->
    <div class="card">
        <h3>Terms & Conditions</h3>
        <ol>
            <li>All information submitted during agent registration and deposit/withdrawal requests must be completely accurate and authentic.</li>
            <li>Agents must maintain professional conduct and strictly adhere to PayGaid operational guidelines and security protocols.</li>
            <li>Any fraudulent activity, unauthorized access attempts, or violation of financial compliance will result in immediate suspension of the agent account.</li>
            <li>PayGaid reserves the right to update program terms, commission structures, and operational policies as required to ensure platform integrity.</li>
        </ol>
    </div>

    <!-- 4. Frequently Asked Questions -->
    <div class="card">
        <h3>Frequently Asked Questions</h3>
        
        <div class="faq-item">
            <div class="faq-question">What is PayGaid?</div>
            <div class="faq-answer">PayGaid is a specialized high-risk payment gateway designed to handle secure and efficient financial transactions for specialized industries like iGaming and international commerce.</div>
        </div>

        <div class="faq-item" style="margin-top: 12px;">
            <div class="faq-question">How do I become a PayGaid Agent?</div>
            <div class="faq-answer">You can register through our official Telegram bot, submit your verification details, and access the agent portal dashboard to start operations.</div>
        </div>

        <div class="faq-item" style="margin-top: 12px;">
            <div class="faq-question">How are deposits and withdrawals processed?</div>
            <div class="faq-answer">All deposits and withdrawals are handled via automated request modules integrated directly inside our secure platform dashboard and Telegram mini app.</div>
        </div>

        <div class="faq-item" style="margin-top: 12px;">
            <div class="faq-question">Where can I get support if I face issues?</div>
            <div class="faq-answer">You can reach out to our dedicated support team through the contact options available inside the portal or via our official communication channels.</div>
        </div>
    </div>

    <div class="footer">
        Powered by PayGaid
    </div>
</div>

</body>
</html>
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(pro_content)
    print("Professional international UI template applied successfully!")
else:
    print("index.html not found!")
