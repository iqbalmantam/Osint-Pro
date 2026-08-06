import httpx
import asyncio
from urllib.parse import quote

# Mapping Platform dan Format Direct URL serta Domain Dork
PLATFORMS_CONFIG = {
    "LinkedIn": {
        "domain": "linkedin.com/in/",
        "direct_tmpl": "https://www.google.com/search?q=site:linkedin.com/in/+{}"
    },
    "Instagram": {
        "domain": "instagram.com",
        "direct_tmpl": "https://www.instagram.com/{}/"
    },
    "TikTok": {
        "domain": "tiktok.com",
        "direct_tmpl": "https://www.tiktok.com/@{}"
    },
    "X (Twitter)": {
        "domain": "x.com",
        "direct_tmpl": "https://x.com/{}"
    },
    "Threads": {
        "domain": "threads.net",
        "direct_tmpl": "https://www.threads.net/@{}"
    },
    "Spotify": {
        "domain": "open.spotify.com/user/",
        "direct_tmpl": "https://open.spotify.com/user/{}"
    },
    "GitHub": {
        "domain": "github.com",
        "direct_tmpl": "https://github.com/{}"
    },
    "Pinterest": {
        "domain": "pinterest.com",
        "direct_tmpl": "https://www.pinterest.com/{}/"
    },
    "Dev.to": {
        "domain": "dev.to",
        "direct_tmpl": "https://dev.to/{}"
    },
    "Medium": {
        "domain": "medium.com",
        "direct_tmpl": "https://medium.com/@{}"
    },
    "Telegram": {
        "domain": "t.me",
        "direct_tmpl": "https://t.me/{}"
    }
}

async def _build_entry(name, cfg, raw_input):
    clean = raw_input.strip().replace("@", "")
    if not clean:
        return {
            "platform": name,
            "found": False,
            "direct_url": "#",
            "dork_url": "#",
            "status_note": "❌ Input Kosong"
        }

    clean_no_space = "".join(clean.lower().split())
    
    # Direct Link ke Platform
    direct_link = cfg["direct_tmpl"].format(clean_no_space)
    
    # Dorking Google Search Link
    if " " in clean:
        no_space = "".join(clean.lower().split())
        dash_space = "-".join(clean.lower().split())
        dork_query = f'site:{cfg["domain"]} ({clean} OR "{no_space}" OR "{dash_space}")'
    else:
        dork_query = f'site:{cfg["domain"]} "{clean}"'
        
    dork_link = f"https://www.google.com/search?q={quote(dork_query)}"

    return {
        "platform": name,
        "found": True,
        "direct_url": direct_link,
        "dork_url": dork_link,
        "status_note": f"🔍 Tautan Investigasi Ready"
    }

async def check_indonesia_socials(username: str):
    if not username or not username.strip():
        return []
        
    tasks = [
        _build_entry(name, cfg, username)
        for name, cfg in PLATFORMS_CONFIG.items()
    ]
    
    return await asyncio.gather(*tasks)
