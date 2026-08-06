import httpx
import asyncio
from urllib.parse import quote

# Mapping Domain Target
DORK_DOMAINS = {
    "LinkedIn": "linkedin.com/in/",
    "Instagram": "instagram.com",
    "TikTok": "tiktok.com",
    "X (Twitter)": "x.com OR twitter.com",
    "Threads": "threads.net",
    "Spotify": "open.spotify.com/user/",
    "GitHub": "github.com",
    "Pinterest": "pinterest.com",
    "Dev.to": "dev.to",
    "Medium": "medium.com",
    "Telegram": "t.me"
}

def build_smart_dork_query(name: str, domain: str, raw_input: str) -> tuple[str, str]:
    clean = raw_input.strip().replace("@", "")
    if not clean:
        return "", "❌ Input Kosong"
        
    # Handling Khusus Telegram: Direct Link + Deep Search (100% Anti Error)
    if name == "Telegram":
        clean_user = "".join(clean.lower().split())
        direct_url = f"https://t.me/{clean_user}"
        return direct_url, f"✈️ Direct Telegram Protocol (@{clean_user})"

    # Handling Nama Lengkap (Mengandung Spasi)
    if " " in clean:
        no_space = "".join(clean.lower().split())
        dash_space = "-".join(clean.lower().split())
        
        # Sintaks pencarian alami Google
        query = f'site:{domain} ({clean} OR "{no_space}" OR "{dash_space}")'
    else:
        # Jika single username (seperti 'iqbalmantam')
        query = f'site:{domain} {clean}'
        
    google_search_url = f"https://www.google.com/search?q={quote(query)}"
    return google_search_url, f"🔎 Smart Dork: {clean}"

async def _build_dork_entry(name, domain, raw_input):
    clean_input = raw_input.strip().replace("@", "")
    if not clean_input:
        return {
            "platform": name, 
            "found": False, 
            "url": "#", 
            "status_note": "❌ Input Kosong"
        }

    target_url, note = build_smart_dork_query(name, domain, clean_input)

    return {
        "platform": name,
        "found": True,
        "url": target_url,
        "status_note": note
    }

async def check_indonesia_socials(username: str):
    if not username or not username.strip():
        return []
        
    tasks = [
        _build_dork_entry(name, domain, username)
        for name, domain in DORK_DOMAINS.items()
    ]
    
    return await asyncio.gather(*tasks)
