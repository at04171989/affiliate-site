#!/usr/bin/env python3
"""Auto-generate and publish affiliate articles"""
import os, subprocess, json
from datetime import datetime

REPO_DIR = "/home/ubuntu/affiliate-site"
TRACKING_ID = "at04171989-20"
USERNAME = "at04171989"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def run(cmd, cwd=REPO_DIR):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)

# Generate today's article
date = datetime.now().strftime("%Y-%m-%d")
articles = [
    {"title": "提升居家辦公效率必備神器", "tag": "office", "products": ["升降桌", "人體工學椅", "護眼屏幕"]},
    {"title": "2026年最值得入手嘅真無線藍牙耳機", "tag": "audio", "products": ["AirPods Pro 3", "Sony WF-1000XM6", "Samsung Galaxy Buds Pro 3"]},
    {"title": "智能家居入門推薦：由零開始打造智慧家庭", "tag": "smart-home", "products": ["智能燈泡", "智能插座", "智能音箱"]},
]

# Pick article based on date
article = articles[hash(date) % len(articles)]

article_html = f'''
<div class="article">
    <div class="date">{date}</div>
    <h2>{article["title"]}</h2>
    <p>今日為你推薦：{", ".join(article["products"])}。點擊以下連結去Amazon了解更多...</p>
    <a class="cta-btn" href="https://www.amazon.com/s?k={article["products"][0]}&tag={TRACKING_ID}" target="_blank">🔍 睇更多</a>
</div>
'''

# Read existing index.html
with open(f"{REPO_DIR}/index.html", "r") as f:
    content = f.read()

# Insert new article at top of #articles div
old = '<div id="articles">'
new = f'<div id="articles">{article_html}'
content = content.replace(old, new)

# Keep only latest 20 articles
import re
articles_found = re.findall(r'<div class="article">.*?</div>\s*</div>', content, re.DOTALL)
if len(articles_found) > 20:
    # Keep first 20
    first_article = content.index('<div class="article">')
    last_20th = content.index('<div class="article">', first_article)
    for _ in range(20):
        last_20th = content.index('<div class="article">', last_20th + 1) if '<div class="article">' in content[last_20th+1:] else last_20th
    # This needs more care... for now just write

with open(f"{REPO_DIR}/index.html", "w") as f:
    f.write(content)

# Git push
run("git add .")
run(f'git commit -m "Auto article - {date}"')
if TOKEN:
    run(f"git push https://{USERNAME}:{TOKEN}@github.com/{USERNAME}/affiliate-site.git main")
else:
    # Try with embedded token in git config
    run("git push origin main")

print(f"Published: {article['title']} - {date}")
