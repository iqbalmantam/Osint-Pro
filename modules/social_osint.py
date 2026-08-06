import httpx
import asyncio
from urllib.parse import quote

# Mapping Platform ke Query Dorking Terisolasi
DORK_TEMPLATES = {
    "LinkedIn": 'site:linkedin.com/in/ "{}"',
    "Instagram": 'site:instagram.com "{}"',
    "TikTok": 'site:tiktok.com/@ "{}"',
    "X (Twitter)": 'site:x.com OR site:twitter.com "{}"',
    "Threads": 'site:threads.net/@ "{}"',
    "Spotify": 'site:open.spotify.com/user/ "{}"',
    "GitHub": 'site:github.com "{}"',
    "Pinterest": 'site:pinterest.com "{}"',
    "Dev.to": 'site:dev.to "{}"',
    "Medium": 'site:medium.com/@ "{}"',
    "Telegram": 'site:t.me "{}"'
}

async def _build_dork_entry(name, dork_pattern, raw_input):
    clean_input = raw_input.strip().replace("@", "")
    if not clean_input:
        return {
            "platform": name, 
            "found": False, 
            "url": "#", 
            "status_note": "❌ Input Kosong"
        }

    # Susun query dorking
    query = dork_pattern.format(clean_input)
    google_search_url = f"https://www.google.com/search?q={quote(query)}"

    return {
        "platform": name,
        "found": True,  # Selalu valid sebagai tautan investigasi presisi
        "url": google_search_url,
        "status_note": f"🔎 Google Precision Dork: {clean_input}"
    }

async def check_indonesia_socials(username: str):
    if not username or not username.strip():
        return []
        
    tasks = [
        _build_dork_entry(name, pattern, username)
        for name, pattern in DORK_TEMPLATES.items()
    ]
    
    return await asyncio.gather(*tasks)
