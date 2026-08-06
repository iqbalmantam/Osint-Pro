from urllib.parse import quote_plus


def generate_pddikti_dorks(target_input, company_or_city=""):
  """Membangun Google Dorking dan Direct Link khusus PDDikti & Rekam Akademik Indonesia."""
  if not target_input:
    return []

  clean_target = target_input.strip()
  dorks = []

  extra_str = f' "{company_or_city.strip()}"' if company_or_city else ""

  # Jika ada spasi (nama lengkap), bungkus dengan kutip ganda. Jika username, gunakan string langsung.
  formatted_target = (
      f'"{clean_target}"' if " " in clean_target else clean_target
  )

  # 1. PDDikti Direct Google Dork
  q_pddikti = (
      "site:pddikti.kemdiktisaintek.go.id OR site:pddikti.kemdikbud.go.id"
      f" {formatted_target}{extra_str}"
  )
  dorks.append({
      "title": (
          "🎓 Verifikasi Data Mahasiswa / Alumni PDDikti Kemenristekdikti"
          " (Google Index)"
      ),
      "query": q_pddikti,
      "link": f"https://www.google.com/search?q={quote_plus(q_pddikti)}&nfpr=1",
  })

  # 2. Skripsi & Repository Kampus (.ac.id)
  q_repo = (
      f"site:ac.id (filetype:pdf OR filetype:doc) {formatted_target}{extra_str}"
  )
  dorks.append({
      "title": (
          "📚 Pindai Karya Ilmiah & Skripsi di Repository Kampus (.ac.id)"
      ),
      "query": q_repo,
      "link": f"https://www.google.com/search?q={quote_plus(q_repo)}&nfpr=1",
  })

  # 3. Direct Search Link Portal PDDikti (Manual Input Search)
  direct_pddikti_url = f"https://pddikti.kemdiktisaintek.go.id/search/{quote_plus(clean_target)}"
  dorks.append({
      "title": "🏛️ Akses Direct Portal Pencarian PDDikti Resmi",
      "query": f"Direct Query -> {clean_target}",
      "link": direct_pddikti_url,
  })

  return dorks
