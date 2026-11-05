path = "/var/www/app/main.py"
with open(path, "r", encoding="utf-8") as f:
    code = f.read()

# নিশ্চিত করা হচ্ছে যাতে get_db ফাংশনটি ফাইলে অবশ্যই থাকে
get_db_definition = '''
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''

if "def get_db(" not in code:
    # কোডের ওপরের দিকে বা ইমপোর্টের পরে এটি বসিয়ে দেওয়া হচ্ছে
    code = code.replace("app = FastAPI()", "app = FastAPI()\n\n" + get_db_definition.strip())

with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print("get_db function fixed successfully!")
