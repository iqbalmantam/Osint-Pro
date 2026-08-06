from urllib.parse import quote_plus

def generate_indonesia_dorks(email_in, phone_data, username_in, name_in, city_in="", company_in=""):
    target_name = name_in.strip() if name_in else ""
    target_user = username_in.strip() if username_in else ""
    target_email = email_in.strip() if email_in else ""
    phone_clean = phone_data.get("local_format", "").strip()
    
    city_str = f' "{city_in.strip()}"' if city_in else ""
    comp_str = f' "{company_in.strip()}"' if company_in else ""
    context_str = f"{city_str}{comp_str}"

    dorks = []

    # 1. Legal & Court Search (Mahkamah Agung / SIPP)
    if target_name:
        q_legal = f'(site:mahkamahagung.go.id OR site:pn-*.go.id OR site:pt-*.go.id) "{target_name}"{context_str}'
        dorks.append({
            "title": "⚖️ Pindai Rekam Jejak Hukum & Perkara Pengadilan (MA / SIPP)",
            "query": q_legal,
            "link": f"https://www.google.com/search?q={quote_plus(q_legal)}&nfpr=1"
        })

    # 2. PDF & Document Leak Search
    doc_query_parts = []
    if target_name:
        doc_query_parts.append(f'"{target_name}"')
    if target_email:
        doc_query_parts.append(f'"{target_email}"')
    if phone_clean:
        doc_query_parts.append(f'"{phone_clean}"')
        
    if doc_query_parts:
        q_doc = f"(filetype:pdf OR filetype:xlsx OR filetype:docx) ({' OR '.join(doc_query_parts)}){context_str}"
        dorks.append({
            "title": "📄 Pencarian Dokumen Publik & File Sensitif (PDF/XLSX)",
            "query": q_doc,
            "link": f"https://www.google.com/search?q={quote_plus(q_doc)}&nfpr=1"
        })

    # 3. Mention Berita & Forum Publik
    target_kw = f'"{target_name}"' if target_name else (f'"{target_user}"' if target_user else "")
    if target_kw:
        q_news = f"(site:detik.com OR site:kompas.com OR site:kaskus.co.id OR site:kumparan.com) {target_kw}{context_str}"
        dorks.append({
            "title": "📰 Pindai Penyebutan Nama di Media Berita & Forum Publik",
            "query": q_news,
            "link": f"https://www.google.com/search?q={quote_plus(q_news)}&nfpr=1"
        })

    # 4. Global Footprint
    if target_user:
        q_global = f'"{target_user}"'
        dorks.append({
            "title": "🌐 Pindai Jejak Digital Global (Username Eksak di Seluruh Web)",
            "query": q_global,
            "link": f"https://www.google.com/search?q={quote_plus(q_global)}&nfpr=1"
        })

    return dorks

def generate_telecom_dorks(phone_intl):
    """Membangun tautan eksternal lookup caller ID publik & direct portal."""
    clean_phone = phone_intl.replace("+", "").replace(" ", "").strip()
    
    return {
        "truecaller": f"https://www.truecaller.com/search/id/{clean_phone}",
        "getcontact": f"https://www.getcontact.com/en/know-who-is-calling?number=%2B{clean_phone}",
        "syncme": f"https://sync.me/search/?number={clean_phone}"
    }
