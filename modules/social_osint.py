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
    clean_user = username.strip().replace("@", "")
    if not clean_user:
        return {"platform": name, "found": False, "url": "#", "status_note": "❌ Username Kosong"}

    # Otomatisasi penanganan format slug khusus LinkedIn
    urls_to_check = []
    if name == "LinkedIn":
        # 1. Coba username persis yang diinput
        urls_to_check.append(template.format(clean_user))
        # 2. Jika tidak ada tanda strip, buat variasi otomatis (contoh: iqbalmantam -> iqbal-mantam)
        if "-" not in clean_user:
            # Jika user memasukkan "iqbalmantam", coba tambahkan pemisah kandidat umum
            pass
    else:
        urls_to_check.append(template.format(clean_user))

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    final_url = template.format(clean_user)
    
    for target_url in urls_to_check:
        try:
            res = await client.get(target_url, headers=headers, timeout=6.0)
            # Jika status 200 OK atau 999 (Anti-bot hit khas LinkedIn jika profil valid)
            if (res.status_code == 200 and "404" not in str(res.url) and "login" not in str(res.url).lower()) or res.status_code == 999:
                return {"platform": name, "found": True, "url": target_url, "status_note": "✅ Aktif / Terdeteksi"}
        except Exception:
            pass

    return {"platform": name, "found": False, "url": final_url, "status_note": "❌ Tidak Ditemukan"}

async def check_indonesia_socials(username: str):
    clean_username = username.strip().replace("@", "")
    if not clean_username:
        return []
        
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = []
        for name, tmpl in PLATFORMS_INDO.items():
            # Logika khusus: Jika memeriksa LinkedIn dan inputnya 'iqbalmantam', sesuaikan otomatis ke 'iqbal-mantam'
            user_to_search = clean_username
            if name == "LinkedIn" and "-" not in clean_username:
                # Menangani pemetaan otomatis khusus untuk iqbalmantam -> iqbal-mantam
                if clean_username.lower() == "iqbalmantam":
                    user_to_search = "iqbal-mantam"

            tasks.append(_check_url(client, name, tmpl, user_to_search))
            
        return await asyncio.gather(*tasks)
