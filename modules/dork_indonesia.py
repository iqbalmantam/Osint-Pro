from urllib.parse import quote_plus

DISPOSABLE_DOMAINS = [
    "tempmail.com", "guerrillamail.com", "10minutemail.com", 
    "trashmail.com", "yopmail.com", "mailinator.com", "sharklasers.com"
]

def check_email_disposable(email: str):
    if "@" in email:
        domain = email.split("@")[1].lower()
        if domain in DISPOSABLE_DOMAINS:
            return True, domain
    return False, email.split("@")[1] if "@" in email else ""

def generate_indonesia_dorks(email: str, phone_info: dict, username: str = "", full_name: str = ""):
    dorks = []
    
    if full_name:
        # 1. Verification PDDikti & Academic Records
        q_edu = f'site:pddikti.kemdikbud.go.id "{full_name.strip()}" OR "{full_name.strip()}" "ijazah" OR "wisuda" OR "skck"'
        dorks.append({
            "title": "🎓 Verifikasi Akademik & PDDikti (Pangkalan Data Pendidikan Tinggi)",
            "query": q_edu,
            "link": f"https://www.google.com/search?q={quote_plus(q_edu)}"
        })
        
        # 2. Mahkamah Agung & Court Registry
        q_legal = f'"{full_name.strip()}" site:mahkamahagung.go.id OR "putusan mahkamah agung" OR "terpidana" OR "tergugat"'
        dorks.append({
            "title": "⚖️ Audit Hukum (Direktori Putusan Mahkamah Agung & SIPP PN)",
            "query": q_legal,
            "link": f"https://www.google.com/search?q={quote_plus(q_legal)}"
        })

        # 3. OJK & Financial Compliance Check
        q_fin = f'"{full_name.strip()}" "satgas pasti" OR "ojk" OR "penipuan" OR "investasi bodong" OR "dftr_hitam"'
        dorks.append({
            "title": "🏦 Rekam Jejak Keuangan & Integritas Finansial (OJK / Satgas Pasti)",
            "query": q_fin,
            "link": f"https://www.google.com/search?q={quote_plus(q_fin)}"
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
