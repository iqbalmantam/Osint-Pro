import aiohttp
import hashlib

async def check_email_identity(email):
    if not email:
        return {"gravatar": {"found": False}, "github": {"found": False}}
    
    clean_email = email.strip().lower()
    email_hash = hashlib.md5(clean_email.encode('utf-8')).hexdigest()
    
    res = {
        "gravatar": {"found": False},
        "github": {"found": False}
    }
    
    async with aiohttp.ClientSession() as session:
        # 1. Gravatar API Check
        gravatar_url = f"https://www.gravatar.com/{email_hash}.json"
        try:
            async with session.get(gravatar_url, timeout=5) as g_resp:
                if g_resp.status == 200:
                    g_data = await g_resp.json()
                    entry = g_data['entry'][0]
                    res["gravatar"] = {
                        "found": True,
                        "display_name": entry.get('displayName', 'N/A'),
                        "about": entry.get('aboutMe', 'Tidak ada bio'),
                        "avatar": entry.get('thumbnailUrl', f"https://www.gravatar.com/avatar/{email_hash}?s=200"),
                        "profile_url": entry.get('profileUrl', f"https://gravatar.com/{email_hash}")
                    }
        except Exception:
            pass
            
        # 2. GitHub User Search
        gh_url = f"https://api.github.com/search/users?q={clean_email}+in:email"
        try:
            headers = {"Accept": "application/vnd.github.v3+json", "User-Agent": "OSINT-Engine/4.0"}
            async with session.get(gh_url, headers=headers, timeout=5) as gh_resp:
                if gh_resp.status == 200:
                    gh_data = await gh_resp.json()
                    if gh_data.get('total_count', 0) > 0:
                        user = gh_data['items'][0]
                        res["github"] = {
                            "found": True,
                            "username": user.get('login'),
                            "avatar": user.get('avatar_url'),
                            "profile_url": user.get('html_url'),
                            "repos": "Tersedia",
                            "bio": "Akun Developer Terverifikasi",
                            "company": "N/A"
                        }
        except Exception:
            pass
            
    return res
