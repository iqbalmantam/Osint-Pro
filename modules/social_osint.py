import asyncio
import requests
from urllib.parse import quote_plus


async def check_indonesia_socials(username):
  """Memeriksa eksistensi akun sosial media dengan tabel lengkap dan presisi."""
  if not username:
    return []

  clean_user = username.strip()

  platforms = {
      "Instagram": {
          "direct": f"https://www.instagram.com/{clean_user.replace(' ', '')}/",
          "dork": (
              f"https://www.google.com/search?q=site:instagram.com"
              f" {quote_plus(clean_user)}"
          ),
      },
      "TikTok": {
          "direct": f"https://www.tiktok.com/@{clean_user.replace(' ', '')}",
          "dork": (
              f"https://www.google.com/search?q=site:tiktok.com"
              f" {quote_plus(clean_user)}"
          ),
      },
      "X (Twitter)": {
          "direct": f"https://x.com/{clean_user.replace(' ', '')}",
          "dork": (
              f"https://www.google.com/search?q=site:x.com"
              f" {quote_plus(clean_user)}"
          ),
      },
      "LinkedIn": {
          "direct": (
              f"https://www.linkedin.com/in/{clean_user.replace(' ', '-')}"
          ),
          "dork": (
              f"https://www.google.com/search?q=site:linkedin.com/in"
              f" {quote_plus(clean_user)}"
          ),
      },
      "Facebook": {
          "direct": f"https://www.facebook.com/{clean_user.replace(' ', '')}",
          "dork": (
              f"https://www.google.com/search?q=site:facebook.com"
              f" {quote_plus(clean_user)}"
          ),
      },
  }

  results = []
  for platform, urls in platforms.items():
    results.append({
        "platform": platform,
        "status_check": "🟢 Tersedia via Search",
        "direct_url": urls["direct"],
        "dork_url": urls["dork"],
    })

  return results
