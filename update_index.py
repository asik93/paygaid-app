file_path = "/var/www/app/index.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# নিশ্চিত করা হচ্ছে যাতে onclick ফাংশনগুলো সঠিকভাবে কাজ করে
old_target = 'onclick="selectCountry(\'India\''
if old_target in content:
    print("Country click handlers already exist.")
else:
    print("Replacing country onclick attributes...")

# সম্পূর্ণ ফাইলটি পুনরায় ঠিক করে সেভ করা হচ্ছে
