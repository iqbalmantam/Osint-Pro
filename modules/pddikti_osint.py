from urllib.parse import quote_plus

def generate_pddikti_dorks(name_in, company_or_city=""):
    if not name_in:
        return []
    
    clean_name = name_in.strip()
    dorks = []
    
    extra_str = f' "{company_or_city.strip()}"' if company_or_city else ""
    
    # 1. PDDikti Direct Dork
    q_pddikti = f'site:pddikti.kemdiktisaintek.go.id OR site:pddikti.kemdikbud.go.id "{clean_name}"{extra_str}'
    dorks.append({
        "title": "🎓 Verifikasi Data Mahasiswa / Alumni PDDikti Kemenristekdikti",
        "query": q_pddikti,
        "link": f"https://www.google.com/search?q={quote_plus(q_pddikti)}&nfpr=1"
    })
    
    # 2. Skripsi & Repository Kampus (.ac.id)
    q_repo = f'site:*.ac.id (filetype:pdf OR filetype:doc) "{clean_name}"{extra_str}'
    dorks.append({
        "title": "📚 Pindai Karya Ilmiah & Skripsi di Repository Kampus (.ac.id)",
        "query": q_repo,
        "link": f"https://www.google.com/search?q={quote_plus(q_repo)}&nfpr=1"
    })
    
    return dorks
