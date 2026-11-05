import os

file_path = "/var/www/app/index.html"
if os.path.exists(file_path):
    print("index.html file verified successfully.")
else:
    print("index.html not found.")
