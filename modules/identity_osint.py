import httpx
import hashlib

async def check_email_identity(email: str):
    clean_email = email.strip().lower()
    email_hash = hashlib.md5(clean_email.encode()).hexdigest()
    
    results = {"gravatar": {"found": False}, "github": {"found": False}}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    async with httpx.AsyncClient(timeout=6.0, follow_redirects=True, headers=headers) as client:
        # Gravatar Check
        try:
            res = await client.get(f"https://en.gravatar.com/{email_hash}.json")
            if res.status_code == 200:
                entry = res.json().get("entry", [{}])[0]
                results["gravatar"] = {
                    "found": True,
                    "profile_url": entry.get("profileUrl", f"https://gravatar.com/{email_hash}"),
                    "display_name": entry.get("displayName", "-"),
                    "avatar": entry.get("thumbnailUrl", ""),
                    "about": entry.get("aboutMe", "Tidak ada bio publik")
                }
        except Exception:
            pass

        # GitHub Check
        try:
            res = await client.get(f"https://api.github.com/search/users?q={clean_email}+in:email")
            if res.status_code == 200:
                items = res.json().get("items", [])
                if items:
                    user = items[0]
                    u_res = await client.get(user["url"])
                    detail = u_res.json() if u_res.status_code == 200 else {}
                    results["github"] = {
                        "found": True,
                        "username": user.get("login"),
                        "profile_url": user.get("html_url"),
                        "avatar": user.get("avatar_url"),
                        "repos": detail.get("public_repos", 0),
                        "bio": detail.get("bio", "-"),
                        "company": detail.get("company", "-")
                    }
        except Exception:
            pass

    return results
