from urllib.parse import quote_plus

def generate_indonesia_dorks(email: str, phone_info: dict, username: str = "", full_name: str = ""):
    dorks = []
    
    if email:
        q = f'"{email.strip()}"'
        dorks.append({
            "title": "📜 Rekam Jejak Email (PDF Ijazah / Sertifikat / PDF Public)",
            "query": q,
            "link": f"https://www.google.com/search?q={quote_plus(q)}"
        })

    if phone_info:
        q = f'"{phone_info["local_format"]}" OR "{phone_info["intl_format"]}"'
        dorks.append({
            "title": "📱 Jejak Kontak Seluler (Forum / GetContact Logs / Marketplace)",
            "query": q,
            "link": f"https://www.google.com/search?q={quote_plus(q)}"
        })

    if full_name:
        q_legal = f'"{full_name.strip()}" site:mahkamahagung.go.id OR "putusan" OR "terpidana"'
        dorks.append({
            "title": "⚖️ Audit Rekam Jejak Hukum (Direktori Putusan Mahkamah Agung)",
            "query": q_legal,
            "link": f"https://www.google.com/search?q={quote_plus(q_legal)}"
        })
        
        q_edu = f'"{full_name.strip()}" "ijazah" OR "wisuda" OR "PDDikti" OR "skck"'
        dorks.append({
            "title": "🎓 Verifikasi Akademik & Administrasi (PDDikti / Wisuda / SKCK)",
            "query": q_edu,
            "link": f"https://www.google.com/search?q={quote_plus(q_edu)}"
        })

    if username:
        clean_u = username.replace("@", "").strip()
        q_user = f'"{clean_u}" -site:instagram.com -site:twitter.com -site:linkedin.com'
        dorks.append({
            "title": "🔍 Forum External & Mentions Username @" + clean_u,
            "query": q_user,
            "link": f"https://www.google.com/search?q={quote_plus(q_user)}"
        })

    return dorks
