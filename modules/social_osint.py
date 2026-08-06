import httpx
import asyncio
from urllib.parse import quote

DORK_DOMAINS = {
    "LinkedIn": "linkedin.com/in/",
    "Instagram": "instagram.com",
    "TikTok": "tiktok.com",
    "X (Twitter)": "x.com OR site:twitter.com",
    "Threads": "threads.net",
    "Spotify": "open.spotify.com/user/",
    "GitHub": "github.com",
    "Pinterest": "pinterest.com",
    "Dev.to": "dev.to",
    "Medium": "medium.com",
    "Telegram": "t.me"
}

def generate_multi_anchor_query(domain: str, raw_username: str, email: str = "") -> str:
    clean_name = raw_username.strip().replace("@", "")
    queries_parts = []
    
    # Extract Email Prefix
    email_prefix = ""
    if email and "@" in email:
        email_prefix = email.split("@")[0].strip().lower()

    if clean_name:
        no_space = "".join(clean_name.lower().split())
        dash_space = "-".join(clean_name.lower().split())
        queries_parts.append(f'"{clean_name}"')
        queries_parts.append(f'"{no_space}"')
        queries_parts.append(f'"{dash_space}"')

    if email_prefix and email_prefix not in queries_parts:
        queries_parts.append(f'"{email_prefix}"')

    combined = " OR ".join(queries_parts) if queries_parts else f'"{clean_name}"'
    return f'site:{domain} ({combined})'

async def _build_dork_entry(name, domain, raw_username, email):
    clean_input = raw_username.strip().replace("@", "")
    if not clean_input and not email:
        return {
            "platform": name, 
            "found": False, 
            "url": "#", 
            "status_note": "❌ Input Kosong"
        }

    query = generate_multi_anchor_query(domain, clean_input, email)
    google_search_url = f"https://www.google.com/search?q={quote(query)}"

    return {
        "platform": name,
        "found": True,
        "url": google_search_url,
        "status_note": f"🔎 Deep Dork Multi-Anchor"
    }

async def check_indonesia_socials(username: str, email: str = ""):
    tasks = [
        _build_dork_entry(name, domain, username, email)
        for name, domain in DORK_DOMAINS.items()
    ]
    return await asyncio.gather(*tasks)
