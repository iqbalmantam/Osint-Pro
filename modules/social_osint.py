import httpx
import asyncio
import re

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

def _generate_username_variations(username: str) -> list:
    clean = username.strip().replace("@", "")
    variations = [clean]
    
    # Jika tidak ada tanda strip/titik, buat variasi otomatis (contoh: iqbalmantam -> iqbal-mantam)
    if "-" not in clean and "." not in clean:
        # Coba sisipkan dash jika ada camelCase atau pola kata
        split_words = re.findall(r'[A-Z]?[a-z]+|[0-9]+', clean)
        if len(split_words) > 1:
            variations.append("-".join(split_words).lower())
            
    return list(set(variations))

async def _check_single_platform(client, name, template, username):
    clean_user = username.strip().replace("@", "")
    
    # Untuk LinkedIn & Medium, uji variasi dengan dash jika variasi biasa gagal
    targets_to_try = [clean_user]
    if name in ["LinkedIn", "Medium"] and "-" not in clean_user and "." not in clean_user:
        # Tambahkan variasi pemisah otomatis untuk nama umum
        pass

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    url = template.format(clean_user)
    try:
        res = await client.get(url, headers=headers, timeout=6.0)
        
        # Penanganan Status Code Khusus
        if res.status_code == 200 and "login" not in str(res.url).lower():
            return {"platform": name, "found": True, "url": url, "status_note": "✅ Aktif (200 OK)"}
        elif res.status_code == 999:  # LinkedIn Anti-Bot Hit (Profil Ada)
            return {"platform": name, "found": True, "url": url, "status_note": "✅ Terdeteksi (Authwall)"}
    except Exception:
        pass

    return {"platform": name, "found": False, "url": url, "status_note": "❌ Tidak Ditemukan"}

async def check_indonesia_socials(username: str):
    clean_username = username.strip().replace("@", "")
    if not clean_username:
        return []
        
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = []
        for name, tmpl in PLATFORMS_INDO.items():
            tasks.append(_check_single_platform(client, name, tmpl, clean_username))
            
        return await asyncio.gather(*tasks)
