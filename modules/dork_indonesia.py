from urllib.parse import quote_plus

def generate_precise_dorks(name_in):
    """Menghasilkan dork yang berfokus pada dokumen/file."""
    if not name_in: 
        return []
        
    query = f'"{name_in}" (filetype:pdf OR filetype:docx OR filetype:xlsx)'
    
    return [{
        "title": "📄 Pencarian Dokumen Forensik (PDF/DOCX)",
        "query": query,
        "link": f"https://www.google.com/search?q={quote_plus(query)}"
    }]

def generate_telecom_dorks(intl_format):
    """Fungsi ini tetap diperlukan oleh app.py untuk lookup nomor telepon."""
    clean_intl = intl_format.strip() if intl_format else ""
    return {
        "truecaller": f"https://www.truecaller.com/search/in/{clean_intl.replace('+', '')}",
        "getcontact": "https://www.getcontact.com/en/search",
        "syncme": "https://sync.me/",
    }
