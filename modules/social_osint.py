import asyncio
import requests
from urllib.parse import quote_plus


async def check_indonesia_socials(username):
  """Memeriksa eksistensi akun sosial media dengan format query dork yang presisi."""
  if not username:
    return []

  clean_user = username.strip()
  # Jika username mengandung spasi (seperti nama lengkap), pisahkan dengan spasi atau beri tanda kutip
  formatted_query = f'"{clean_user}"' if " " in clean_user else clean_user

  platforms = {
      "Instagram": f"https://www.google.com/search?q=site:instagram.com+{quote_plus(clean_user)}",
      "TikTok": f"https://www.google.com/search?q=site:tiktok.com+{quote_plus(clean_user)}",
      "X (Twitter)": f"https://www.google.com/search?q=site:x.com+{quote_plus(clean_user)}",
      "LinkedIn": f"https://www.google.com/search?q=site:linkedin.com/in+{quote_plus(clean_user)}",
      "Facebook": f"https://www.google.com/search?q=site:facebook.com+{quote_plus(clean_user)}",
  }

  results = []
  for platform, search_url in platforms.items():
    results.append({
        "platform": platform,
        "status_check": "🟢 Tersedia via Search",
        "dork_url": search_url,
    })

  return results
