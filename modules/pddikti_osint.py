from urllib.parse import quote_plus


def generate_pddikti_dorks(target_init, company_or_city="", nim_in=""):
  """Membangun tautan pencarian langsung kategori Mahasiswa/Dosen dan Dorking rekam akademik."""
  if not target_init and not nim_in:
    return []

  dorks = []
  clean_target = target_init.strip() if target_init else ""
  clean_nim = nim_in.strip() if nim_in else ""

  # 1. Direct Search Kategori Mahasiswa via NIM (Paling Akurat)
  if clean_nim:
    direct_mhs_nim = f"https://pddikti.kemdiktisaintek.go.id/data/student/{quote_plus(clean_nim)}"
    dorks.append({
        "title": "🎯 [MAHASISWA] Verifikasi Langsung via NIM di PDDikti",
        "query": f"Direct Student NIM -> {clean_nim}",
        "link": direct_mhs_nim,
    })

  # 2. Direct Search Kategori Mahasiswa via Keyword / Nama
  if clean_target:
    direct_mhs_keyword = f"https://pddikti.kemdiktisaintek.go.id/search/{quote_plus(clean_target)}"
    dorks.append({
        "title": "🎓 [MAHASISWA] Verifikasi Portal Resmi PDDikti (Keyword Search)",
        "query": f"Direct Keyword -> {clean_target}",
        "link": direct_mhs_keyword,
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
