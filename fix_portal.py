import os

file_path = "/var/www/app/main.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# index.html er bodole country selection ba main start page file- ti set korar jnno route update kora
# Apnar project er country selection page-er file name 'agent-dashboard.html' ba 'index.html' er moddhe kon ti hobe seta niche change kore dicchi
new_route = """
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    # Prothome agent-dashboard ba country selection page khuje set kora
    for fname in ["agent-dashboard.html", "index.html"]:
        if os.path.exists(fname):
            with open(fname, "r", encoding="utf-8") as file:
                html_content = file.read()
                if "Select your Country" in html_content or "Country" in html_content:
                    return html_content
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
print("Main portal route successfully updated to show country selection!")
