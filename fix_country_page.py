import os

file_path = "/var/www/app/main.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Country selection page-ti je file- e ache setake root route- e set kora
new_route = """
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    # Prothome country selection ba page1 file khuje ber kora
    for fname in ["page1_start.html", "index.html", "agent-dashboard.html"]:
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8") as file:
                html_content = file.read()
                if "Select your Country" in html_content:
                    return html_content
    # Jodi file na paoa jay tahole index.html return korbe
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as file:
            return file.read()
    return "Page not found"
"""

import re
content = re.sub(r"@app\.get\(\"\/\"\).*?return.*?(?=\n\n@|\Z)", "", content, flags=re.DOTALL)
content += new_route

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Root route updated successfully to country selection page!")
