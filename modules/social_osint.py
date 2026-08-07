import asyncio
from urllib.parse import quote_plus

async def check_indonesia_socials(query_target):
    """Memeriksa eksistensi akun sosial media dengan membungkus query menggunakan tanda kutip."""
    if not query_target:
        return []

    clean_target = query_target.strip()
    
    # Membungkus target dengan tanda kutip ganda agar Google mencari string utuh berisis spasi (misal: "Iqbal Mantam")
    quoted_query = f'"{clean_target}"'

    platforms = {
        "Instagram": f"https://www.google.com/search?q=site:instagram.com+{quote_plus(quoted_query)}",
        "TikTok": f"https://www.google.com/search?q=site:tiktok.com+{quote_plus(quoted_query)}",
        "X (Twitter)": f"https://www.google.com/search?q=site:x.com+{quote_plus(quoted_query)}",
        "LinkedIn": f"https://www.google.com/search?q=site:linkedin.com/in+{quote_plus(quoted_query)}",
        "Facebook": f"https://www.google.com/search?q=site:facebook.com+{quote_plus(quoted_query)}",
    }

    results = []
    for platform, search_url in platforms.items():
        results.append({
            "platform": platform,
            "status_check": "🟢 Tersedia via Search",
            "dork_url": search_url
        })

    return results
