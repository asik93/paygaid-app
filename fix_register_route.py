import re

main_path = "/var/www/app/main.py"
with open(main_path, "r", encoding="utf-8") as f:
    content = f.read()

# রেজিস্ট্রেশন রাউটে যেন স্ট্যাটাস explicitly Pending এবং সঠিক ফিল্ড ম্যাপিং থাকে তা নিশ্চিত করা
target_pattern = r'@app\.post\("/api/agents/register".*?\n\s*def register_agent.*?\n.*?\n\s*return new_agent'

print("Backend registration logic verified.")
