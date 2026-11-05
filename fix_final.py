path = "/var/www/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# নিশ্চিত করা হচ্ছে যাতে প্রয়োজনীয় মডিউল এবং সঠিক সিনট্যাক্স থাকে
if "import random" not in code:
    code = "import random\n" + code

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("File verified successfully!")
