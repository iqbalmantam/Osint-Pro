import httpx
import asyncio
from urllib.parse import quote

# Mapping Domain Target
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

def build_smart_dork_query(domain: str, raw_input: str) -> str:
    clean = raw_input.strip().replace("@", "")
    if not clean:
        return ""
        
    # Penanganan Khusus Telegram: Langsung ke path username tanpa sintaks OR berulang
    if domain == "t.me":
        clean_no_space = "".join(clean.lower().split())
        return f'site:t.me/{clean_no_space} OR site:t.me "{clean}"'

    # Untuk platform lain: Buat variasi unik (tanpa duplikasi)
    if " " in clean:
        no_space = "".join(clean.lower().split())
        dash_space = "-".join(clean.lower().split())
        
        # Menggunakan dict.fromkeys untuk menjaga urutan sekaligus menghilangkan duplikat
        unique_terms = list(dict.fromkeys([f'"{clean}"', f'"{no_space}"', f'"{dash_space}"']))
        combined = " OR ".join(unique_terms)
        return f'site:{domain} ({combined})'
    else:
        return f'site:{domain} "{clean}"'

async def _build_dork_entry(name, domain, raw_input):
    clean_input = raw_input.strip().replace("@", "")
    if not clean_input:
        return {
            "platform": name, 
            "found": False, 
            "url": "#", 
            "status_note": "❌ Input Kosong"
        }

    query = build_smart_dork_query(domain, clean_input)
    google_search_url = f"https://www.google.com/search?q={quote(query)}"

    return {
        "platform": name,
        "found": True,
        "url": google_search_url,
        "status_note": f"🔎 Precision Dork: {clean_input}"
    }

async def check_indonesia_socials(username: str):
    if not username or not username.strip():
        return []
        
    tasks = [
        _build_dork_entry(name, domain, username)
        for name, domain in DORK_DOMAINS.items()
    ]
    
    return await asyncio.gather(*tasks)
