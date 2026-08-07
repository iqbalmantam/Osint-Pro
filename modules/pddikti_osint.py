from urllib.parse import quote_plus


def generate_pddikti_dorks(target_input, company_or_city="", nim_in=""):
  """Membangun tautan pencarian langsung berbasis NIM/Nama dan Dorking rekam akademik."""
  if not target_input and not nim_in:
    return []

  dorks = []
  clean_target = target_input.strip() if target_input else ""
  clean_nim = nim_in.strip() if nim_in else ""

  # 1. Jika NIM diisi, arahkan langsung ke query NIM (100% akurat tanpa reCAPTCHA blocking URL)
  if clean_nim:
    direct_pddikti_url = f"https://pddikti.kemdiktisaintek.go.id/search/{quote_plus(clean_nim)}"
    dorks.append({
        "title": "🎯 [HIGH ACCURACY] Verifikasi Langsung via NIM di Portal PDDikti",
        "query": f"Direct NIM Query -> {clean_nim}",
        "link": direct_pddikti_url,
    })

  # 2. Direct Search Link Portal PDDikti berbasis Nama/Keyword
  if clean_target:
    direct_pddikti_url = f"https://pddikti.kemdiktisaintek.go.id/search/{quote_plus(clean_target)}"
    dorks.append({
        "title": "🏛️ Verifikasi Portal Resmi PDDikti (Keyword Search)",
        "query": f"Direct Query -> {clean_target}",
        "link": direct_pddikti_url,
    })

  # 3. Google Dorking Cadangan (Repository Kampus / ac.id)
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
