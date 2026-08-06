import aiohttp
from urllib.parse import quote_plus


def build_clean_dork_url(domain, target_input):
    """Membangun URL Google Dork yang valid dengan pembungkus tanda petik ganda

    pada setiap frasa/kata untuk mencegah hasil kosong di Google.
    """
    if not target_input:
        return "#"

    clean_target = target_input.strip()
    keywords = [f'"{clean_target}"']

    if " " in clean_target:
        no_space = clean_target.replace(" ", "")
        hyphen_space = clean_target.replace(" ", "-")
        keywords.append(f'"{no_space}"')
        keywords.append(f'"{hyphen_space}"')

    query = f"site:{domain} (" + " OR ".join(keywords) + ")"
    return f"https://www.google.com/search?q={quote_plus(query)}"


async def check_indonesia_socials(target_input):
    """Memeriksa keberadaan profil medsos dan menghasilkan link dorking presisi."""
    if not target_input:
        return []

    clean_handle = target_input.strip().replace(" ", "")

    platforms = [
        {
            "platform": "Instagram",
            "domain": "instagram.com",
            "direct_url": f"https://www.instagram.com/{clean_handle}/",
        },
        {
            "platform": "TikTok",
            "domain": "tiktok.com",
            "direct_url": f"https://www.tiktok.com/@{clean_handle}",
        },
        {
            "platform": "X (Twitter)",
            "domain": "x.com",
            "direct_url": f"https://x.com/{clean_handle}",
        },
        {
            "platform": "Threads",
            "domain": "threads.net",
            "direct_url": f"https://www.threads.net/@{clean_handle}",
        },
        {
            "platform": "Spotify",
            "domain": "open.spotify.com",
            "direct_url": f"https://open.spotify.com/user/{clean_handle}",
        },
        {
            "platform": "LinkedIn",
            "domain": "linkedin.com",
            "direct_url": f"https://www.linkedin.com/in/{clean_handle}",
        },
        {
            "platform": "Facebook",
            "domain": "facebook.com",
            "direct_url": f"https://www.facebook.com/{clean_handle}",
        },
        {
            "platform": "Pinterest",
            "domain": "pinterest.com",
            "direct_url": f"https://www.pinterest.com/{clean_handle}",
        },
    ]

    results = []

    # Asynchronous HEAD/GET Request untuk memverifikasi ketersediaan profil
    async with aiohttp.ClientSession() as session:
        for p in platforms:
            dork_url = build_clean_dork_url(p["domain"], target_input)
            status_label = "🟡 Perlu Diulas Manual"

            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                async with session.get(
                    p["direct_url"], headers=headers, timeout=5, allow_redirects=True
                ) as resp:
                    if resp.status == 200:
                        status_label = "🟢 Terverifikasi Ada"
                    elif resp.status in [404, 410]:
                        status_label = "🔴 Pasti Tidak Ada"
            except Exception:
                status_label = "🟡 Perlu Diulas Manual"

            results.append(
                {
                    "platform": p["platform"],
                    "status_check": status_label,
                    "direct_url": p["direct_url"],
                    "dork_url": dork_url,
                }
            )

    return results
