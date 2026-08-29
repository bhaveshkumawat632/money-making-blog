import os
import sys
import datetime
import requests
import json
import random
import subprocess

PEXELS_KEY = os.environ.get("PEXELS_API_KEY", "cBBsobTILBswJ5myAoj74hr3Vw2ylE4zUpXCRtbLsrQGvGvzPQYGEEzf")
BLOG_DIR = "/home/junglee01/money-making-blog/src/content/blog"

TOPICS = [
    ("How Automated Agents are Replacing Junior Devs in 2026", "technology software ai"),
    ("The Next Crypto Bull Run: Why Utility Tokens Are Back", "crypto finance money"),
    ("Building a $10k/mo Passive Income Stack with Free Tools", "business passive income"),
]

def get_cover_image(query):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    headers = {"Authorization": PEXELS_KEY}
    try:
        res = requests.get(url, headers=headers).json()
        return res['photos'][0]['src']['landscape']
    except Exception as e:
        return "https://images.pexels.com/photos/730564/pexels-photo-730564.jpeg?auto=compress&cs=tinysrgb&w=800"

def generate():
    os.makedirs(BLOG_DIR, exist_ok=True)
    title, query = random.choice(TOPICS)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = title.lower().replace(" ", "-").replace("/", "").replace("$", "")
    
    img = get_cover_image(query)
    
    content = f"""---
title: '{title}'
description: 'Discover the latest strategies and insights for 2026 on {title.lower()}.'
pubDate: '{datetime.datetime.now().strftime("%b %d %Y")}'
heroImage: '{img}'
---

In 2026, the digital landscape is changing faster than ever. What used to take a team of experts now takes a single autonomous agent. 
If you want to stay ahead, you need to understand the mechanics of the new wealth engines.

## The Paradigm Shift

Most people are still operating on the 2020 playbook. They think creating content requires hours of manual research, writing, and editing.
The reality is that **autonomous architectures** have made manual work obsolete.

Here is what the top 1% are doing:
1. **Delegation to AI:** Using multi-agent systems to research and draft.
2. **Review & Approve:** Only spending time on quality control.
3. **Automated Deployment:** Pushing changes directly via CI/CD pipelines.

## How to Get Started Today

If you haven't already, start setting up your own autonomous agents. Whether it's for YouTube Shorts or SEO blogging, the barrier to entry has never been lower.

> "The secret to financial freedom in 2026 isn't saving money. It's building automated systems."

Stay tuned for more insights, and don't forget to subscribe to the WealthAutomater newsletter.
"""

    filepath = os.path.join(BLOG_DIR, f"{slug}.md")
    with open(filepath, "w") as f:
        f.write(content)
        
    print(f"✅ Generated article: {filepath}")
    
    # Auto commit
    subprocess.run(["git", "add", "."], cwd="/home/junglee01/money-making-blog")
    subprocess.run(["git", "commit", "-m", f"Auto-publish: {title}"], cwd="/home/junglee01/money-making-blog")
    # subprocess.run(["git", "push"], cwd="/home/junglee01/money-making-blog")

if __name__ == "__main__":
    generate()
