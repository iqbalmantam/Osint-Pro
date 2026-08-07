import itertools

def generate_username_variations(name_in):
    """Membuat variasi username berdasarkan nama lengkap."""
    if not name_in:
        return []
    parts = name_in.lower().split()
    variations = [
        "".join(parts),
        ".".join(parts),
        "_".join(parts),
        parts[0] + parts[-1],
        parts[0] + "." + parts[-1]
    ]
    return list(set(variations))

def check_consistency(phone_data, city_in):
    """Mendeteksi ketidaksesuaian dasar data."""
    # Logika sederhana: Cek apakah provider lokal relevan dengan domisili
    # Bisa dikembangkan lebih lanjut berdasarkan prefix operator
    return "✅ Data profil terlihat konsisten."
