from urllib.parse import quote_plus


def generate_pddikti_dorks(target_input, company_or_city=""):
  """Membangun tautan pencarian langsung dan Google Dorking rekam akademik."""
  if not target_input:
    return []

  clean_target = target_input.strip()
  dorks = []

  extra_str = f' "{company_or_city.strip()}"' if company_or_city else ""
  formatted_target = (
      f'"{clean_target}"' if " " in clean_target else clean_target
  )

  # 1. Direct Search Link Portal PDDikti (Paling Akurat untuk Database SPA)
  direct_pddikti_url = f"https://pddikti.kemdiktisaintek.go.id/search/{quote_plus(clean_target)}"
  dorks.append({
      "title": (
          "🏛️ [RECOMMENDED] Verifikasi Langsung di Database Portal Resmi"
          " PDDikti"
      ),
      "query": f"Direct Query -> {clean_target}",
      "link": direct_pddikti_url,
  })

  # 2. Google Dorking Cadangan (Repository Kampus / ac.id)
  q_repo = (
      f"site:ac.id (filetype:pdf OR filetype:doc) {formatted_target}{extra_str}"
  )
  dorks.append({
      "title": "📚 Pindai Karya Ilmiah & Skripsi di Repository Kampus (.ac.id)",
      "query": q_repo,
      "link": f"https://www.google.com/search?q={quote_plus(q_repo)}&nfpr=1",
  })

  return dorks
