import asyncio
import requests
from urllib.parse import quote_plus


async def check_indonesia_socials(username):
  """Memeriksa eksistensi akun sosial media secara akurat."""
  if not username:
    return []

  clean_user = username.strip().replace("@", "")

  # Daftar platform dengan format URL profil langsung dan Google Dork cadangan yang valid
  platforms = {
      "Instagram": {
          "direct": f"https://www.instagram.com/{clean_user}/",
          "search": f"https://www.google.com/search?q=site:instagram.com {clean_user}",
      },
      "TikTok": {
          "direct": f"https://www.tiktok.com/@{clean_user}",
          "search": f"https://www.google.com/search?q=site:tiktok.com {clean_user}",
      },
      "X (Twitter)": {
          "direct": f"https://x.com/{clean_user}",
          "search": f"https://www.google.com/search?q=site:x.com {clean_user}",
      },
      "LinkedIn": {
          "direct": f"https://www.linkedin.com/in/{clean_user}",
          "search": (
              f"https://www.google.com/search?q=site:linkedin.com/in"
              f" {clean_user}"
          ),
      },
      "Facebook": {
          "direct": f"https://www.facebook.com/{clean_user}",
          "search": f"https://www.google.com/search?q=site:facebook.com {clean_user}",
      },
  }

  results = []
  for platform, urls in platforms.items():
    try:
      # Pengecekan HTTP Request ringan
      headers = {"User-Agent": "Mozilla/5.0"}
      response = requests.get(urls["direct"], headers=headers, timeout=4)

      if response.status_code == 200:
        status = "🟢 Terverifikasi Ada"
        final_url = urls["direct"]
      else:
        status = "🟡 Cek via Search"
        final_url = urls["search"]

      results.append({
          "platform": platform,
          "status_check": status,
          "direct_url": final_url,
      })
    except:
      results.append({
          "platform": platform,
          "status_check": "🟡 Cek via Search",
          "direct_url": urls["search"],
      })

  return results
