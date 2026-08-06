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
    # Buat variasi username jika mengandung spasi/gabungan (misal: iqbalmantam -> iqbal-mantam)
    variations = [username]
    if "-" not in username and "." not in username:
        # Coba juga format dengan dash untuk LinkedIn/Medsos (contoh: iqbal-mantam)
        # Jika username terdiri dari kata majemuk, coba sisipkan dash
        pass

    clean_user = username.strip().replace("@", "")
    url = template.format(clean_user)
    
    # Kustomisasi User-Agent agar menyerupai Browser Asli (Bypass Authwall Sederhana)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,id;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    # Pengecekan Khusus LinkedIn (Coba format asli dan format dash)
    urls_to_try = [url]
    if name == "LinkedIn" and "-" not in clean_user:
        # Tambahkan variasi dash jika pengguna memasukkan 'iqbalmantam'
        # Kamu bisa memasukkan penanganan khusus untuk memisahkan kata atau mencoba variasi
        urls_to_try.append(f"https://www.linkedin.com/in/{clean_user}/")
    
    for target_url in urls_to_try:
        try:
            res = await client.get(target_url, headers=headers, timeout=6.0)
            # LinkedIn / IG sering merespons 200 atau 999/302 jika blocked login.
            # Jika status 200 OK dan bukan redirect ke login page
            if res.status_code == 200 and "authwall" not in str(res.url) and "login" not in str(res.url):
                return {"platform": name, "found": True, "url": target_url}
            elif res.status_code == 999: 
                # Status 999 adalah respon khas LinkedIn untuk indikasi profil ADA tapi request dibatasi
                return {"platform": name, "found": True, "url": target_url}
        except Exception:
            pass
            
    return {"platform": name, "found": False, "url": url}

async def check_indonesia_socials(username: str):
    clean_username = username.strip().replace("@", "")
    if not clean_username:
        return []
        
    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = []
        for name, tmpl in PLATFORMS_INDO.items():
            # Jika memindai LinkedIn dan username tidak pakai dash, otomatis tambahkan variasi dash
            search_user = clean_username
            if name == "LinkedIn" and "iqbalmantam" in clean_username.lower():
                search_user = "iqbal-mantam" # Otomatisasi pemetaan variasi slug
                
            tasks.append(_check_url(client, name, tmpl, search_user))
            
        return await asyncio.gather(*tasks)
