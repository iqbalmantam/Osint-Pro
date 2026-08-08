import httpx

async def search_pddikti(query):
    """Melakukan pencarian data mahasiswa/dosen melalui PDDikti API publik."""
    if not query:
        return {"status": "error", "message": "Query kosong"}
    
    base_url = "https://pddikti.rone.dev/api"
    results = {"mahasiswa": [], "dosen": []}
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # 1. Cari Mahasiswa
            mhs_res = await client.get(f"{base_url}/search/mahasiswa", params={"q": query})
            if mhs_res.status_code == 200:
                results["mahasiswa"] = mhs_res.json()
        except:
            pass

        try:
            # 2. Cari Dosen
            dosen_res = await client.get(f"{base_url}/search/dosen", params={"q": query})
            if dosen_res.status_code == 200:
                results["dosen"] = dosen_res.json()
        except:
            pass

    return results
