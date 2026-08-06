import re

PREFIX_MAP = {
    "Telkomsel": ["0811", "0812", "0813", "0821", "0822", "0823", "0851", "0852", "0853"],
    "Indosat Ooredoo": ["0814", "0815", "0816", "0855", "0856", "0857", "0858"],
    "XL Axiata": ["0817", "0818", "0819", "0859", "0877", "0878"],
    "Axis": ["0831", "0832", "0833", "0838"],
    "Smartfren": ["0881", "0882", "0883", "0884", "0885", "0886", "0887", "0888", "0889"],
    "Tri (3)": ["0895", "0896", "0897", "0898", "0899"]
}

def analyze_indonesia_phone(phone_raw: str):
    clean = re.sub(r"[^\d]", "", phone_raw)
    
    if clean.startswith("62"):
        formatted_local = "0" + clean[2:]
        formatted_intl = clean
    elif clean.startswith("0"):
        formatted_local = clean
        formatted_intl = "62" + clean[1:]
    else:
        formatted_local = "0" + clean
        formatted_intl = "62" + clean

    prefix = formatted_local[:4]
    detected_provider = "Tidak Diketahui / Provider Luar"
    for provider, prefixes in PREFIX_MAP.items():
        if prefix in prefixes:
            detected_provider = provider
            break

    return {
        "raw": phone_raw,
        "local_format": formatted_local,
        "intl_format": formatted_intl,
        "provider": detected_provider,
        "wa_link": f"https://wa.me/{formatted_intl}",
        "telegram_link": f"https://t.me/+{formatted_intl}"
    }
