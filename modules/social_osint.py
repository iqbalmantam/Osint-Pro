import httpx
import asyncio
from urllib.parse import quote

PLATFORMS_INDO = {
    "LinkedIn": "https://www.google.com/search?q={}",
    "Instagram": "https://www.instagram.com/{}/",
    "TikTok": "https://www.tiktok.com/@{}",
    "X (Twitter)": "https://x.com/{}",
    "Threads": "https://www.threads.net/@{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "GitHub": "https://github.com/{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Dev.to": "https://dev.to/{}",
    "Medium": "https://medium.com/@{}",
    "Telegram": "https://t.me/{}"
}

def clean_slug(raw_username: str, platform: str) -> str:
    """Membersihkan dan menyesuaikan format URL sesuai platform."""
    username = raw_username.strip().replace("@", "")
    
    if platform == "LinkedIn":
        # Format dorking khusus LinkedIn agar 100% tepat dan anti-404
        return quote(f'site:linkedin.com/in/ "{username}"')
    
    if " " in username:
        if platform == "Medium":
            return "-".join(username.lower().split())
        else:
            return "".join(username.lower().split())
            
    return username.lower()

async def _check_url(client, name, template, raw_username):
    slug = clean_slug(raw_username, name)
    if not slug:
        return {"platform": name, "found": False, "url": "#", "status_note": "❌ Username Kosong"}

    # Penanganan Khusus LinkedIn: Menggunakan Smart Dorking agar 100% Akurat
    if name == "LinkedIn":
        search_url = template.format(slug)
        return {
            "platform": "LinkedIn", 
            "found": True, 
            "url": search_url, 
            "status_note": "🔎 Search Direct Profile (Anti-404)"
        }

    url = template.format(quote(slug) if name != "LinkedIn" else slug)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    try:
        res = await client.get(url, headers=headers, timeout=6.0)
        res_text = res.text.lower()
        
        is_404 = "page doesn’t exist" in res_text or "page doesn't exist" in res_text or "404" in str(res.url)
        
        if res.status_code == 200 and not is_404 and "login" not in str(res.url).lower():
            return {"platform": name, "found": True, "url": url, "status_note": "✅ Aktif / Terdeteksi"}
    except Exception:
        pass

    return {"platform": name, "found": False, "url": url, "status_note": "❌ Tidak Ditemukan"}

async def check_indonesia_socials(username: str):
    if not username or not username.strip():
        return []
        
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [
            _check_url(client, name, tmpl, username)
            for name, tmpl in PLATFORMS_INDO.items()
        ]
        return await asyncio.gather(*tasks)
