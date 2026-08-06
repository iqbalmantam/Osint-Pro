import re

def analyze_indonesia_phone(phone_str):
    if not phone_str:
        return {
            "provider": "Unknown",
            "local_format": "-",
            "intl_format": "-",
            "wa_link": "#",
            "telegram_link": "#"
        }
    
    clean_num = re.sub(r'\D', '', phone_str)
    if clean_num.startswith('0'):
        clean_num = '62' + clean_num[1:]
    elif not clean_num.startswith('62'):
        clean_num = '62' + clean_num
        
    local_fmt = '0' + clean_num[2:]
    
    prefix = local_fmt[:4]
    provider = "Lainnya / Seluler Indonesia"
    
    telkomsel = ['0811', '0812', '0813', '0821', '0822', '0823', '0851', '0852', '0853']
    indosat = ['0814', '0815', '0816', '0855', '0856', '0857', '0858']
    xl_axis = ['0817', '0818', '0819', '0859', '0877', '0878', '0838', '0831', '0832', '0833']
    three = ['0895', '0896', '0897', '0898', '0899']
    smartfren = ['0881', '0882', '0883', '0884', '0885', '0886', '0887', '0888', '0889']
    
    if prefix in telkomsel:
        provider = "Telkomsel"
    elif prefix in indosat:
        provider = "Indosat Ooredoo Hutchison"
    elif prefix in xl_axis:
        provider = "XL / AXIS"
    elif prefix in three:
        provider = "Tri (3)"
    elif prefix in smartfren:
        provider = "Smartfren"
        
    return {
        "provider": provider,
        "local_format": local_fmt,
        "intl_format": f"+{clean_num}",
        "raw_clean": clean_num,
        "wa_link": f"https://wa.me/{clean_num}",
        "telegram_link": f"https://t.me/+{clean_num}"
    }
