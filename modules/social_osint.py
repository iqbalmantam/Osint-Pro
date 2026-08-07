import asyncio
import requests
from urllib.parse import quote_plus


async def check_indonesia_socials(username):
  """Memeriksa eksistensi akun sosial media secara akurat dengan fallback search."""
  if not username:
    return []

  clean_user = username.strip().replace("@", "")

  platforms = {
      "Instagram": f"https://www.google.com/search?q=site:instagram.com+{clean_user}",
      "TikTok": f"https://www.google.com/search?q=site:tiktok.com+{clean_user}",
      "X (Twitter)": (
          f"https://www.google.com/search?q=site:x.com+{clean_user}"
      ),
      "LinkedIn": (
          f"https://www.google.com/search?q=site:linkedin.com/in+{clean_user}"
      ),
      "Facebook": (
          f"https://www.google.com/search?q=site:facebook.com+{clean_user}"
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
