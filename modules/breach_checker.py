import httpx

async def check_data_breach(email: str):
    clean_email = email.strip().lower()
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{clean_email}?truncateResponse=false"
    headers = {"User-Agent": "Candidate-OSINT-App"}
    
    async with httpx.AsyncClient(timeout=6.0) as client:
        try:
            res = await client.get(url, headers=headers)
            if res.status_code == 200:
                return {"email": clean_email, "breached": True, "data": res.json()}
            elif res.status_code == 404:
                return {"email": clean_email, "breached": False, "data": []}
        except Exception:
            pass
    return {"email": clean_email, "breached": False, "data": [], "error": "Pengecekan dibatasi/timeout"}
