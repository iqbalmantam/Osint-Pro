from urllib.parse import quote_plus

def generate_pddikti_dorks(target_init, company_or_city="", nim_in=""):
    if not target_init and not nim_in:
        return []

    dorks = []
    clean_target = target_init.strip() if target_init else ""
    clean_nim = nim_in.strip() if nim_in else ""
    
    # Prioritas NIM jika ada, jika tidak pakai Nama/Username
    primary_query = clean_nim if clean_nim else clean_target

    # 1. Official Portal Link
    dorks.append({
        "title": "🏛️ [OFFICIAL] Buka Portal PDDikti (Klik, lalu PASTE query di bawah)",
        "query": primary_query, 
        "link": "https://pddikti.kemdiktisaintek.go.id/"
    })

    # 2. Google Dorking Cadangan
    if clean_target:
        formatted_target = f'"{clean_target}"' if " " in clean_target else clean_target
        q_repo = f"site:ac.id (filetype:pdf OR filetype:doc) {formatted_target}"
        dorks.append({
            "title": "📚 Pindai Karya Ilmiah/Skripsi (.ac.id)",
            "query": q_repo,
            "link": f"https://www.google.com/search?q={quote_plus(q_repo)}&nfpr=1"
        })

    return dorks
