from urllib.parse import quote_plus


def generate_pddikti_dorks(target_init, company_or_city="", nim_in=""):
  """Membangun tautan pencarian langsung ke portal resmi PDDikti dan rekam akademik."""
  if not target_init and not nim_in:
    return []

  dorks = []
  clean_target = target_init.strip() if target_init else ""
  clean_nim = nim_in.strip() if nim_in else ""

  # Target prioritas untuk pre-fill / referensi pencarian
  primary_query = clean_nim if clean_nim else clean_target

  # 1. Direct Link ke Beranda Utama PDDikti (Portal Resmi Bebas Error 404)
  if primary_query:
    direct_portal_url = (
        "https://pddikti.kemdiktisaintek.go.id/?q="
        f"{quote_plus(primary_query)}"
    )
    dorks.append({
        "title": "🏛️ [OFFICIAL] Buka Portal Utama PDDikti",
        "query": f"Portal Query -> {primary_query}",
        "link": direct_portal_url,
    })

  # 2. Google Dorking Cadangan (Repository Kampus / ac.id)
  if clean_target:
    extra_str = f' "{company_or_city.strip()}"' if company_or_city else ""
    formatted_target = (
        f'"{clean_target}"' if " " in clean_target else clean_target
    )
    q_repo = (
        f"site:ac.id (filetype:pdf OR filetype:doc) {formatted_target}{extra_str}"
    )
    dorks.append({
        "title": "📚 Pindai Karya Ilmiah & Skripsi di Repository Kampus (.ac.id)",
        "query": q_repo,
        "link": f"https://www.google.com/search?q={quote_plus(q_repo)}&nfpr=1",
    })

  return dorks
