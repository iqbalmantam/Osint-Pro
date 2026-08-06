from urllib.parse import quote_plus


def generate_pddikti_dorks(target_input, company_or_city=""):
  """Membangun Google Dorking khusus PDDikti & Rekam Akademik Indonesia.

  Dapat menerima input berupa Nama Lengkap ataupun Username.
  """
  if not target_input:
    return []

  clean_target = target_input.strip()
  dorks = []

  extra_str = f' "{company_or_city.strip()}"' if company_or_city else ""

  # Format target (jika mengandung spasi dibungkus tanda petik ganda)
  formatted_target = (
      f'"{clean_target}"' if " " in clean_target else clean_target
  )

  # 1. PDDikti Direct Dork
  q_pddikti = (
      "site:pddikti.kemdiktisaintek.go.id OR site:pddikti.kemdikbud.go.id"
      f" {formatted_target}{extra_str}"
  )
  dorks.append({
      "title": (
          "🎓 Verifikasi Data Mahasiswa / Alumni PDDikti Kemenristekdikti"
      ),
      "query": q_pddikti,
      "link": f"https://www.google.com/search?q={quote_plus(q_pddikti)}&nfpr=1",
  })

  # 2. Skripsi & Repository Kampus (.ac.id) - Menggunakan site:ac.id yang valid
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

  return dorks
