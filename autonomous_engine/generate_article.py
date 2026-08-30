import os
import sys
import datetime
import requests
import json
import random
import subprocess

PEXELS_KEY = os.environ.get("PEXELS_API_KEY", "cBBsobTILBswJ5myAoj74hr3Vw2ylE4zUpXCRtbLsrQGvGvzPQYGEEzf")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(BASE_DIR, "src", "content", "blog")

TOPICS = [
    {
        "title": "How Autonomous Agents are Replacing Junior Devs in 2026",
        "query": "artificial intelligence code",
        "intro": "The software engineering landscape has undergone a seismic shift. We are no longer debating whether AI will replace coding jobs; we are witnessing the complete automation of the junior developer role. In this deep dive, we explore how autonomous agent architectures are executing full sprint tickets, writing tests, and deploying code without human intervention.",
        "p1": "Traditional development teams required a massive hierarchy: senior engineers to architect, mid-level engineers to build features, and junior engineers to fix bugs and write boilerplate. Today, the bottom tier of that hierarchy has been completely abstracted away by multi-agent systems.",
        "p2": "An autonomous agent doesn't just autocomplete code. It reads the Jira ticket, clones the repository, navigates the codebase, writes the logic, runs the unit tests, and submits a Pull Request. This reduces the deployment cycle from weeks to minutes.",
        "p3": "For those entering the industry, the skill is no longer 'writing code.' The skill is 'orchestrating systems.' If you can architect the prompts and manage the API routing, you are managing a digital workforce.",
        "conclusion": "The future belongs to the orchestrators. The time to adapt to agentic workflows is not tomorrow; it was yesterday."
    },
    {
        "title": "Building a $10k/mo Passive Income Stack with Free Tools",
        "query": "passive income wealth",
        "intro": "The barrier to entry for digital entrepreneurship has hit absolute zero. In 2026, you do not need venture capital, you do not need employees, and you barely need a budget. You only need the right architecture. This guide outlines the exact free tools required to build a system that scales infinitely.",
        "p1": "The first step is separating your time from your output. As long as you are trading hours for dollars, you cannot scale. We achieve separation by building 'Content Engines'—systems that generate organic traffic 24/7 without active input.",
        "p2": "Using open-source models for content generation and GitHub Actions for free CI/CD deployment, you can host incredibly complex SaaS platforms or affiliate blogs at exactly $0/month. The hosting infrastructure provided by modern edge networks has completely democratized scale.",
        "p3": "Once the traffic is secured, monetization is automated via programmatic advertising (like AdSense) and algorithmic affiliate routing. The machine works while you sleep. The key is consistency and technical patience—most quit right before the compounding effect takes over.",
        "conclusion": "Your goal should be to build one digital asset per week. Over a year, the compound interest of your digital real estate will surpass any salary."
    },
    {
        "title": "Why SEO in 2026 is All About AI Agents",
        "query": "seo marketing tech",
        "intro": "Search Engine Optimization is dead. At least, the 2020 version of it is. Backlinks, keyword stuffing, and spun content no longer work against Google's core AI updates. Today, SEO is a battle of autonomous agents. Here is how the top marketers are winning.",
        "p1": "Modern search engines do not read text; they understand concepts. To rank, your content must satisfy 'Search Intent' better than a human could write it. This requires massive datasets and logical structuring—tasks perfectly suited for Agentic AI.",
        "p2": "We are seeing the rise of 'Swarm SEO'. Instead of writing one article, an orchestrator agent spawns 50 sub-agents. They research competitors, extract missing semantic entities, format perfect markdown, and deploy entirely unique, highly authoritative pillars of content across a domain in minutes.",
        "p3": "If you are manually typing out articles hoping to rank, you are competing against data centers. The only way to survive is to become an orchestrator. Deploy your own swarms to maintain topic authority in your niche.",
        "conclusion": "Embrace the swarm. The internet is now machine-to-machine communication; ensure your machines are the smartest."
    }
]

def get_cover_image(query):
    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    headers = {"Authorization": PEXELS_KEY}
    try:
        res = requests.get(url, headers=headers).json()
        return res['photos'][0]['src']['landscape']
    except Exception as e:
        return "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=2000"

def generate():
    os.makedirs(BLOG_DIR, exist_ok=True)
    topic = random.choice(TOPICS)
    title = topic["title"]
    
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    slug = title.lower().replace(" ", "-").replace("/", "").replace("$", "").replace(":", "")
    
    img = get_cover_image(topic["query"])
    
    content = f"""---
title: "{title}"
description: "{topic['intro'][:120]}..."
pubDate: "{datetime.datetime.now().strftime("%b %d %Y")}"
heroImage: "{img}"
---

{topic['intro']}

## The Paradigm Shift

{topic['p1']}

## Execution and Architecture

{topic['p2']}

{topic['p3']}

## Final Thoughts

> "{topic['conclusion']}"

If you want to stay ahead of the curve, you must fundamentally change your relationship with technology. Stop consuming, and start architecting.
"""

    filepath = os.path.join(BLOG_DIR, f"{slug}.md")
    with open(filepath, "w") as f:
        f.write(content)
        
    print(f"✅ Generated HIGH-QUALITY article: {filepath}")

if __name__ == "__main__":
    generate()
