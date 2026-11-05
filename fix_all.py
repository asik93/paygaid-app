path = "/var/www/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# স্ট্যাটাস ইমপোর্ট নিশ্চিত করা এবং কোড ক্লিন করা
if "from fastapi import" in code and "status" not in code:
    code = code.replace("from fastapi import", "from fastapi import status,")

code = code.replace("status_code=status.HTTP_201_CREATED", "status_code=201")

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("Main file cleaned successfully!")
