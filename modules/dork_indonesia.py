from urllib.parse import quote_plus


def generate_indonesia_dorks(
    email_in, phone_data, username_in, name_in, city_in, company_in
):
  """Membuat daftar Google Dork yang aman dan bersih untuk investigasi OSINT."""
  dorks = []
  clean_name = name_in.strip() if name_in else ""
  clean_email = email_in.strip() if email_in else ""
  clean_phone = phone_data.get("local_format", "") if phone_data else ""
  clean_username = username_in.strip() if username_in else ""

  # 1. Dorking Nama Lengkap di Portal Berita & Forum (Dipisah agar tidak blank)
  if clean_name:
    query_name = f'"{clean_name}" site:detik.com OR site:kompas.com OR site:kumparan.com'
    dorks.append({
        "title": "📰 Pindai Nama di Portal Berita Nasional",
        "query": query_name,
        "link": f"https://www.google.com/search?q={quote_plus(query_name)}",
    })

  # 2. Dorking Jejak Email Publik
  if clean_email:
    query_email = f'"{clean_email}"'
    dorks.append({
        "title": "📧 Pindai Jejak Email di Web Publik",
        "query": query_email,
        "link": f"https://www.google.com/search?q={quote_plus(query_email)}",
    })

  # 3. Dorking Nomor Telepon
  if clean_phone:
    query_phone = f'"{clean_phone}"'
    dorks.append({
        "title": "📞 Pindai Nomor Kontak di Internet",
        "query": query_phone,
        "link": f"https://www.google.com/search?q={quote_plus(query_phone)}",
    })

  # 4. Dorking Username / Handle Medsos
  if clean_username:
    query_user = f'"{clean_username}"'
    dorks.append({
        "title": "🌐 Pindai Username di Berbagai Platform",
        "query": query_user,
        "link": f"https://www.google.com/search?q={quote_plus(query_user)}",
    })

  return dorks


def generate_telecom_dorks(intl_format):
  """Menghasilkan tautan lookup nomor telepon."""
  clean_intl = intl_format.strip() if intl_format else ""
  return {
      "truecaller": f"https://www.truecaller.com/search/in/{clean_intl.replace('+', '')}",
      "getcontact": "https://www.getcontact.com/en/search",
      "syncme": "https://sync.me/",
  }
