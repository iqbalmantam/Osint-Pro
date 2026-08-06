from urllib.parse import quote_plus

def generate_indonesia_dorks(email: str = "", phone_info: dict = None, username: str = "", full_name: str = ""):
    dorks = []
    target_name = full_name.strip() if full_name else username.strip()

    if target_name:
        # 1. Verification PDDikti & Academic Records
        q_edu = f'site:pddikti.kemdikbud.go.id "{target_name}" OR "{target_name}" "ijazah" OR "wisuda" OR "skck"'
        dorks.append({
            "title": "🎓 Verifikasi Akademik & PDDikti (Pangkalan Data Pendidikan Tinggi)",
            "query": q_edu,
            "link": f"https://www.google.com/search?q={quote_plus(q_edu)}"
        })
        
        # 2. Mahkamah Agung & Court Registry
        q_legal = f'"{target_name}" site:mahkamahagung.go.id OR "putusan mahkamah agung" OR "terpidana" OR "tergugat"'
        dorks.append({
            "title": "⚖️ Audit Hukum (Direktori Putusan Mahkamah Agung & SIPP PN)",
            "query": q_legal,
            "link": f"https://www.google.com/search?q={quote_plus(q_legal)}"
        })

        # 3. OJK & Financial Compliance Check
        q_fin = f'"{target_name}" "satgas pasti" OR "ojk" OR "penipuan" OR "investasi bodong" OR "dftr_hitam"'
        dorks.append({
            "title": "🏦 Rekam Jejak Keuangan & Integritas Finansial (OJK / Satgas Pasti)",
            "query": q_fin,
            "link": f"https://www.google.com/search?q={quote_plus(q_fin)}"
        })

        # 4. Komunitas & Forum Lokal Indonesia (FITUR BARU)
        q_forum = f'site:kaskus.co.id OR site:id.quora.com OR site:blogspot.com OR site:wordpress.com "{target_name}"'
        dorks.append({
            "title": "💬 Jejak Diskusi Forum & Komunitas Lokal (Kaskus, Quora, Blogspot, WordPress)",
            "query": q_forum,
            "link": f"https://www.google.com/search?q={quote_plus(q_forum)}"
        })

        # 5. E-Commerce & Marketplace Activity (FITUR BARU)
        q_market = f'site:tokopedia.com OR site:shopee.co.id OR site:olx.co.id "{target_name}"'
        dorks.append({
            "title": "🛒 Jejak E-Commerce & Marketplace (Tokopedia, Shopee, OLX)",
            "query": q_market,
            "link": f"https://www.google.com/search?q={quote_plus(q_market)}"
        })

    if email:
        q_email = f'"{email.strip()}"'
        dorks.append({
            "title": "📜 Rekam Jejak Email Publik (PDF / Sertifikat / Dokumen Publik)",
            "query": q_email,
            "link": f"https://www.google.com/search?q={quote_plus(q_email)}"
        })

    if phone_info:
        q_phone = f'"{phone_info["local_format"]}" OR "{phone_info["intl_format"]}"'
        dorks.append({
            "title": "📱 Jejak Kontak Seluler (Forum / Marketplace Logs / Olx)",
            "query": q_phone,
            "link": f"https://www.google.com/search?q={quote_plus(q_phone)}"
        })

    return dorks

def generate_telecom_dorks(phone_intl: str):
    return {
        "getcontact": "https://www.getcontact.com/en/unbind",
        "truecaller": f"https://www.truecaller.com/search/id/{phone_intl}"
    }
