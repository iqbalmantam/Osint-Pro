from urllib.parse import quote_plus


def generate_social_dork_url(platform_domain, target_input):
    """Membangun URL Google Dork yang valid dengan membungkus frasa/nama

    menggunakan tanda petik ganda untuk mencegah pencarian kosong.
    """
    if not target_input:
        return "#"

    target_clean = target_input.strip()
    keywords = []

    # 1. Masukkan input utama dibungkus tanda petik ganda
    keywords.append(f'"{target_clean}"')

    # 2. Jika input mengandung spasi, buat variasi tanpa spasi & dengan tanda hubung (-)
    if " " in target_clean:
        no_space = target_clean.replace(" ", "")
        hyphen_space = target_clean.replace(" ", "-")
        keywords.append(f'"{no_space}"')
        keywords.append(f'"{hyphen_space}"')

    # Gabungkan keyword dengan operator OR di dalam kurung
    query_str = f"site:{platform_domain} (" + " OR ".join(keywords) + ")"

    return f"https://www.google.com/search?q={quote_plus(query_str)}"


def generate_indonesia_dorks(email_in, phone_data, username_in, name_in):
    """Membangun daftar Google Dorks legal & pengadilan Indonesia

    dengan pengutipan frasa yang presisi.
    """
    target_name = name_in.strip() if name_in else ""
    target_user = username_in.strip() if username_in else ""
    target_email = email_in.strip() if email_in else ""
    phone_clean = phone_data.get("local_format", "").strip()

    dorks = []

    # 1. Legal & Court Search (Mahkamah Agung / SIPP / Putusan)
    if target_name:
        q_legal = f'site:mahkamahagung.go.id OR site:pn-*.go.id OR site:pt-*.go.id "{target_name}"'
        dorks.append(
            {
                "title": "⚖️ Pindai Rekam Jejak Hukum & Perkara Pengadilan (MA / SIPP)",
                "query": q_legal,
                "link": f"https://www.google.com/search?q={quote_plus(q_legal)}",
            }
        )

    # 2. PDF & Document Leak Search
    doc_query_parts = []
    if target_name:
        doc_query_parts.append(f'"{target_name}"')
    if target_email:
        doc_query_parts.append(f'"{target_email}"')
    if phone_clean:
        doc_query_parts.append(f'"{phone_clean}"')

    if doc_query_parts:
        q_doc = f"filetype:pdf OR filetype:xlsx OR filetype:docx ({' OR '.join(doc_query_parts)})"
        dorks.append(
            {
                "title": "📄 Pencarian Dokumen Publik & File Sensitif (PDF/XLSX)",
                "query": q_doc,
                "link": f"https://www.google.com/search?q={quote_plus(q_doc)}",
            }
        )

    # 3. Mention Berita & Forum Publik
    if target_name or target_user:
        target_keyword = f'"{target_name}"' if target_name else f'"{target_user}"'
        q_news = f'site:detik.com OR site:kompas.com OR site:kaskus.co.id OR site:kumparan.com {target_keyword}'
        dorks.append(
            {
                "title": "📰 Pindai Penyebutan Nama di Media Berita & Forum Publik",
                "query": q_news,
                "link": f"https://www.google.com/search?q={quote_plus(q_news)}",
            }
        )

    return dorks


def generate_telecom_dorks(phone_intl):
    """Membangun tautan eksternal lookup telecom."""
    clean_phone = phone_intl.replace("+", "").replace(" ", "")
    return {
        "truecaller": f"https://www.truecaller.com/search/id/{clean_phone}",
        "getcontact": "https://www.getcontact.com/",
    }
