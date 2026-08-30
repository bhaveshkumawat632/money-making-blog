import datetime
import json
import os
import random
import re

import requests

PEXELS_KEY = os.environ.get("PEXELS_API_KEY")
BAZAARLINK_API_KEY = os.environ.get("BAZAARLINK_API_KEY")
BAZAARLINK_MODEL = os.environ.get("BAZAARLINK_MODEL", "auto:free")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-20b")
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
MISTRAL_MODEL = os.environ.get("MISTRAL_MODEL", "mistral-small-latest")
LLM7_API_KEY = os.environ.get("LLM7_API_KEY", "unused")
LLM7_MODEL = os.environ.get("LLM7_MODEL", "default")
LLM7_ENABLED = os.environ.get("LLM7_ENABLED", "1") != "0"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(BASE_DIR, "src", "content", "blog")
DEFAULT_COVER_IMAGE = "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=2000"

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
    if not PEXELS_KEY:
        return DEFAULT_COVER_IMAGE

    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"
    headers = {"Authorization": PEXELS_KEY}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        return res.json()["photos"][0]["src"]["landscape"]
    except Exception:
        return DEFAULT_COVER_IMAGE

def slugify(title):
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower())
    return slug.strip("-") or "autonomous-systems-briefing"

def yaml_escape(value):
    return str(value).replace("\\", "\\\\").replace('"', '\\"')

def extract_text_from_gemini(response_json):
    parts = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    return "\n".join(part.get("text", "") for part in parts).strip()

def parse_article_json(raw_text):
    cleaned = raw_text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)

    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Gemini response did not contain a JSON object")

    article = json.loads(cleaned[start:end + 1], strict=False)
    required = ["title", "description", "query", "body_markdown"]
    missing = [field for field in required if not article.get(field)]
    if missing:
        raise ValueError(f"Gemini response missing fields: {', '.join(missing)}")
    return article

def article_prompt():
    return """Create one original, publication-ready article for a premium tech and wealth systems blog.

Return only valid JSON with this exact shape:
{
  "title": "specific SEO title under 70 characters",
  "description": "meta description under 155 characters",
  "query": "two or three words for a relevant cover image search",
  "body_markdown": "1200-1700 words of polished markdown with H2 sections"
}

Editorial rules:
- Audience: builders, operators, and technical founders.
- Tone: mature, precise, premium, no hype, no get-rich-quick claims.
- Topic space: AI agents, autonomous businesses, SEO systems, trading infrastructure, creator monetization, automation.
- Include concrete systems thinking, implementation details, and risks.
- Do not mention that the article was generated by AI.
"""

def generate_with_gemini():
    if not GEMINI_API_KEY:
        return None

    prompt = article_prompt()

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.8,
            "topP": 0.9,
            "maxOutputTokens": 5000,
            "responseMimeType": "application/json",
        },
    }
    headers = {"Content-Type": "application/json"}

    res = requests.post(url, params={"key": GEMINI_API_KEY}, headers=headers, json=payload, timeout=90)
    res.raise_for_status()
    return parse_article_json(extract_text_from_gemini(res.json()))

def extract_openai_chat_text(response_json):
    content = response_json["choices"][0]["message"]["content"]
    if isinstance(content, list):
        return "\n".join(
            item.get("text", "") for item in content if item.get("type") == "text"
        ).strip()
    return content

def generate_with_openai_compatible(name, base_url, api_key, model, extra_headers=None):
    if not api_key:
        return None

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": article_prompt()}],
        "temperature": 0.8,
        "max_tokens": 5000,
        "response_format": {"type": "json_object"},
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    if extra_headers:
        headers.update(extra_headers)

    res = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers=headers,
        json=payload,
        timeout=90,
    )
    res.raise_for_status()
    return parse_article_json(extract_openai_chat_text(res.json()))

def generate_with_bazaarlink():
    return generate_with_openai_compatible(
        "BazaarLink",
        "https://api.bazaarlink.ai/v1",
        BAZAARLINK_API_KEY,
        BAZAARLINK_MODEL,
        {
            "HTTP-Referer": "https://bhaveshkumawat632.github.io/money-making-blog/",
            "X-Title": "Money Making Blog Autonomous Engine",
        },
    )

def generate_with_groq():
    return generate_with_openai_compatible(
        "Groq",
        "https://api.groq.com/openai/v1",
        GROQ_API_KEY,
        GROQ_MODEL,
    )

def generate_with_mistral():
    return generate_with_openai_compatible(
        "Mistral",
        "https://api.mistral.ai/v1",
        MISTRAL_API_KEY,
        MISTRAL_MODEL,
    )

def generate_with_llm7():
    if not LLM7_ENABLED:
        return None
    return generate_with_openai_compatible(
        "LLM7",
        "https://api.llm7.io/v1",
        LLM7_API_KEY,
        LLM7_MODEL,
    )

def generate_with_ai_provider():
    providers = [
        ("BazaarLink", generate_with_bazaarlink),
        ("Groq", generate_with_groq),
        ("Mistral", generate_with_mistral),
        ("LLM7", generate_with_llm7),
        ("Gemini", generate_with_gemini),
    ]
    failures = []

    for name, provider in providers:
        try:
            article = provider()
        except Exception as e:
            failures.append(f"{name}: {e}")
            print(f"{name} generation failed, trying next provider: {e}")
            continue

        if article:
            return article, name

    if failures:
        print("All AI providers failed; using local fallback.")
    return fallback_article(), "fallback"

def fallback_article():
    topic = random.choice(TOPICS)
    return {
        "title": topic["title"],
        "description": f"{topic['intro'][:120]}...",
        "query": topic["query"],
        "body_markdown": f"""{topic['intro']}

## The Paradigm Shift

{topic['p1']}

## Execution and Architecture

{topic['p2']}

{topic['p3']}

## Final Thoughts

> "{topic['conclusion']}"

If you want to stay ahead of the curve, you must fundamentally change your relationship with technology. Stop consuming, and start architecting.
""",
    }

def generate():
    os.makedirs(BLOG_DIR, exist_ok=True)

    article, source = generate_with_ai_provider()

    title = article["title"]
    img = get_cover_image(article["query"])
    body_markdown = article["body_markdown"].strip()

    # --- AFFILIATE MARKETING INJECTION ---
    affiliate_blocks = [
        "\n\n---\n> 🚀 **Scale Your Wealth Systems**: Ready to deploy your own autonomous AI applications? Get up to **75% OFF + Free Domain** with Hostinger.\n> 👉 [Claim Your Premium Hosting Discount Here](https://hostinger.com?ref=autonomous)\n---",
        "\n\n---\n> 📈 **Elite Algo-Trading**: Stop trading with emotions. Deploy quantitative bots and trade securely.\n> 👉 [Join Binance & Claim Your $100 Sign-Up Bonus](https://binance.com/?ref=wealthsystem)\n---",
        "\n\n---\n> 🤖 **Automate Your Attention**: The 1% use AI to scale content. Generate massive traffic automatically.\n> 👉 [Access The Ultimate AI Generator Toolkit](https://jasper.ai?ref=matrix)\n---"
    ]
    chosen_affiliate = random.choice(affiliate_blocks)
    body_markdown += chosen_affiliate
    # -------------------------------------

    content = f"""---
title: "{yaml_escape(title)}"
description: "{yaml_escape(article['description'])}"
pubDate: "{datetime.datetime.now().strftime('%b %d %Y')}"
heroImage: "{yaml_escape(img)}"
---

{body_markdown}
"""

    filepath = os.path.join(BLOG_DIR, f"{slugify(title)}.md")
    with open(filepath, "w") as f:
        f.write(content)

    print(f"Generated article with {source}: {filepath}")

if __name__ == "__main__":
    generate()
