from urllib.parse import quote_plus


def generate_social_dork_url(platform_domain, target_input):
    """Membangun URL Google Dork yang valid dengan pembungkus tanda petik ganda

    dan parameter &nfpr=1 untuk mencegah auto-correct typo oleh Google.
    """
    if not target_input:
        return "#"

    target_clean = target_input.strip()
    keywords = [f'"{target_clean}"']

    if " " in target_clean:
        no_space = target_clean.replace(" ", "")
        hyphen_space = target_clean.replace(" ", "-")
        keywords.append(f'"{no_space}"')
        keywords.append(f'"{hyphen_space}"')

    query_str = f"site:{platform_domain} (" + " OR ".join(keywords) + ")"
    # Tambahkan &nfpr=1 agar Google TIDAK mengoreksi "iqbalmantam" menjadi "iqbal mantan"
    return f"https://www.google.com/search?q={quote_plus(query_str)}&nfpr=1"


def generate_indonesia_dorks(email_in, phone_data, username_in, name_in):
    """Membangun daftar Google Dorks legal & pengadilan Indonesia

    tanpa intervensi auto-correct Google.
    """
    target_name = name_in.strip() if name_in else ""
    target_user = username_in.strip() if username_in else ""
    target_email = email_in.strip() if email_in else ""
    phone_clean = phone_data.get("local_format", "").strip()

    dorks = []

    # 1. Legal & Court Search (Mahkamah Agung / SIPP / Putusan)
    if target_name:
        q_legal = f'(site:mahkamahagung.go.id OR site:pn-*.go.id OR site:pt-*.go.id) "{target_name}"'
        dorks.append(
            {
                "title": "⚖️ Pindai Rekam Jejak Hukum & Perkara Pengadilan (MA / SIPP)",
                "query": q_legal,
                "link": f"https://www.google.com/search?q={quote_plus(q_legal)}&nfpr=1",
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
        q_doc = f"(filetype:pdf OR filetype:xlsx OR filetype:docx) ({' OR '.join(doc_query_parts)})"
        dorks.append(
            {
                "title": "📄 Pencarian Dokumen Publik & File Sensitif (PDF/XLSX)",
                "query": q_doc,
                "link": f"https://www.google.com/search?q={quote_plus(q_doc)}&nfpr=1",
            }
        )

    # 3. Mention Berita & Forum Publik
    if target_name or target_user:
        target_keyword = f'"{target_name}"' if target_name else f'"{target_user}"'
        q_news = f"(site:detik.com OR site:kompas.com OR site:kaskus.co.id OR site:kumparan.com) {target_keyword}"
        dorks.append(
            {
                "title": "📰 Pindai Penyebutan Nama di Media Berita & Forum Publik",
                "query": q_news,
                "link": f"https://www.google.com/search?q={quote_plus(q_news)}&nfpr=1",
            }
        )

    # 4. Global Footprint Eksak (Pencarian Tanpa Filter Domain & Tanpa Koreksi Ejaan)
    if target_user:
        q_global = f'"{target_user}"'
        dorks.append(
            {
                "title": "🌐 Pindai Jejak Digital Global (Username Eksak)",
                "query": q_global,
                "link": f"https://www.google.com/search?q={quote_plus(q_global)}&nfpr=1",
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
