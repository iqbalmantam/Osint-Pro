import aiohttp

async def check_data_breach(email):
    if not email:
        return {"breached": False, "data": []}
    
    # Memeriksa insiden kebocoran publik via API HIBP Alternative
    url = f"https://api.xposedornot.com/v1/check-email/{email.strip()}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if "breaches" in data and len(data["breaches"]) > 0:
                        return {
                            "breached": True,
                            "data": data["breaches"]
                        }
    except Exception:
        pass
        
    return {"breached": False, "data": []}
