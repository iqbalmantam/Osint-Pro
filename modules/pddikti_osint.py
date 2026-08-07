from urllib.parse import quote_plus


def generate_pddikti_dorks(target_init, company_or_city="", nim_in=""):
  """Membangun tautan ke portal resmi PDDikti dan rekam akademik repository."""
  if not target_init and not nim_in:
    return []

  dorks = []
  clean_target = target_init.strip() if target_init else ""
  clean_nim = nim_in.strip() if nim_in else ""

  primary_query = clean_nim if clean_nim else clean_target

  # 1. Official Portal Link dengan teks referensi
  if primary_query:
    dorks.append({
        "title": (
            "🏛️ [OFFICIAL] Portal PDDikti (Salin NIM/Keyword di bawah, lalu"
            " Paste ke Portal)"
        ),
        "query": primary_query,
        "link": "https://pddikti.kemdiktisaintek.go.id/",
    })

  # 2. Google Dorking Cadangan
  if clean_target:
    extra_str = f' "{company_or_city.strip()}"' if company_or_city else ""
    formatted_target = (
        f'"{clean_target}"' if " " in clean_target else clean_target
    )
    q_repo = (
        f"site:ac.id (filetype:pdf OR filetype:doc) {formatted_target}{extra_str}"
    )
    dorks.append({
        "title": "📚 Pindai Karya Ilmiah/Skripsi (.ac.id)",
        "query": q_repo,
        "link": f"https://www.google.com/search?q={quote_plus(q_repo)}&nfpr=1",
    })

  return dorks
