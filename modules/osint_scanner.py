# modules/osint_scanner.py
import requests
import asyncio

async def verify_social_existence(username):
    """Memeriksa eksistensi akun dengan HTTP status check (sangat akurat)."""
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Instagram": f"https://instagram.com/{username}",
        "Twitter": f"https://twitter.com/{username}"
    }
    results = []
    for platform, url in platforms.items():
        try:
            response = requests.get(url, timeout=5)
            # Jika status 200, berarti akun valid/ada
            status = "🟢 Terverifikasi" if response.status_code == 200 else "🔴 Tidak Ditemukan"
            results.append({"platform": platform, "status": status, "url": url})
        except:
            results.append({"platform": platform, "status": "⚠️ Connection Error", "url": url})
    return results
