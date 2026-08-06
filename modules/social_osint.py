import httpx
import asyncio

PLATFORMS_INDO = {
    "LinkedIn": "https://www.linkedin.com/in/{}/",
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

async def _check_url(client, name, template, username):
    url = template.format(username)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        res = await client.get(url, headers=headers, timeout=5.0)
        if res.status_code == 200:
            return {"platform": name, "found": True, "url": url}
    except Exception:
        pass
    return {"platform": name, "found": False, "url": url}

async def check_indonesia_socials(username: str):
    clean_username = username.strip().replace("@", "")
    if not clean_username:
        return []
        
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [
            _check_url(client, name, tmpl, clean_username)
            for name, tmpl in PLATFORMS_INDO.items()
        ]
        return await asyncio.gather(*tasks)
