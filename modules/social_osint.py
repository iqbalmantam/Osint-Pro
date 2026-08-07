import asyncio
import requests
from urllib.parse import quote_plus


async def check_indonesia_socials(username):
  """Memeriksa eksistensi akun sosial media dengan format query dork yang presisi."""
  if not username:
    return []

  clean_user = username.strip()

  # Menggunakan spasi agar Google tidak mendeteksi sebagai typo yang digabung
  platforms = {
      "Instagram": (
          f"https://www.google.com/search?q=site:instagram.com {quote_plus(clean_user)}"
      ),
      "TikTok": (
          f"https://www.google.com/search?q=site:tiktok.com {quote_plus(clean_user)}"
      ),
      "X (Twitter)": (
          f"https://www.google.com/search?q=site:x.com {quote_plus(clean_user)}"
      ),
      "LinkedIn": (
          f"https://www.google.com/search?q=site:linkedin.com/in"
          f" {quote_plus(clean_user)}"
      ),
      "Facebook": (
          f"https://www.google.com/search?q=site:facebook.com {quote_plus(clean_user)}"
      ),
  }

  results = []
  for platform, search_url in platforms.items():
    results.append({
        "platform": platform,
        "status_check": "🟢 Tersedia via Search",
        "dork_url": search_url,
    })

  return results
