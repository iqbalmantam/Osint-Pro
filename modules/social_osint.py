import httpx
import asyncio
from urllib.parse import quote

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

async def _verify_direct_url(client, name, url, clean_user):
    """Mengecek ketersediaan profil secara otomatis di latar belakang."""
    # Hanya LinkedIn yang wajib manual karena authwall pencarian
    if url == "#" or name == "LinkedIn":
        return "🟡 Perlu Diulas Manual"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    try:
        res = await client.get(url, headers=headers, timeout=5.0, follow_redirects=True)
        res_text = res.text.lower()

        # Handling Khusus TikTok
        if name == "TikTok":
            if res.status_code == 200 and ("uniqueid" in res_text or "userinfo" in res_text or clean_user in res_text):
                return "🟢 Terverifikasi Ada"
            elif res.status_code == 404 or 'statuscode":10221' in res_text:
                return "🔴 Pasti Tidak Ada"
            else:
                return "🟡 Perlu Diulas Manual"

        # Deteksi Halaman Kosong/Error untuk Instagram, Threads, X, Spotify, Dev.to, Medium, dll.
        is_404 = (
            res.status_code == 404 or 
            "profile isn't available" in res_text or
            "profile isn’t available" in res_text or
            "page doesn’t exist" in res_text or 
            "page doesn't exist" in res_text or
            "sorry, this page isn't available" in res_text or
            "this user does not exist" in res_text or
            "couldn't find this account" in res_text
        )

        if is_404:
            return "🔴 Pasti Tidak Ada"
        elif res.status_code == 200 and ("login" not in str(res.url).lower() or clean_user in res_text):
            return "🟢 Terverifikasi Ada"
        else:
            return "🟡 Perlu Diulas Manual"
    except Exception:
        return "🟡 Perlu Diulas Manual"

async def _build_entry(client, name, cfg, raw_input):
    clean = raw_input.strip().replace("@", "")
    if not clean:
        return {
            "platform": name,
            "status_check": "❌ Input Kosong",
            "direct_url": "#",
            "dork_url": "#"
        }

    clean_no_space = "".join(clean.lower().split())
    direct_link = cfg["direct_tmpl"].format(clean_no_space)
    
    # Dorking Google Search Query
    if " " in clean:
        no_space = "".join(clean.lower().split())
        dash_space = "-".join(clean.lower().split())
        dork_query = f'site:{cfg["domain"]} ({clean} OR "{no_space}" OR "{dash_space}")'
    else:
        dork_query = f'site:{cfg["domain"]} "{clean}"'
        
    dork_link = f"https://www.google.com/search?q={quote(dork_query)}"

    # Verifikasi Silang Otomatis (HTTP Check)
    status_label = await _verify_direct_url(client, name, direct_link, clean_no_space)

    return {
        "platform": name,
        "status_check": status_label,
        "direct_url": direct_link,
        "dork_url": dork_link
    }

async def check_indonesia_socials(username: str):
    if not username or not username.strip():
        return []
        
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [
            _build_entry(client, name, cfg, username)
            for name, cfg in PLATFORMS_CONFIG.items()
        ]
        return await asyncio.gather(*tasks)
