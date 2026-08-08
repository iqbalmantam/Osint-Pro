import asyncio
import json
import time
from urllib.parse import quote_plus
import pandas as pd
import streamlit as st

from modules.breach_checker import check_data_breach
from modules.dork_indonesia import (
    generate_indonesia_dorks,
    generate_telecom_dorks,
)
from modules.identity_osint import check_email_identity
from modules.indo_telecom import analyze_indonesia_phone
from modules.social_osint import check_indonesia_socials

st.set_page_config(
    page_title="Background Check - OSINT Engine v4.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS UI & Privacy Watermark
st.markdown(
    """
    <style>
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: transparent !important; }
    .watermark { position: fixed; bottom: 15px; left: 50%; transform: translateX(-50%); opacity: 0.85; font-size: 13px; font-weight: 600; color: #8b949e; background-color: rgba(22, 27, 34, 0.9); padding: 6px 18px; border-radius: 20px; border: 1px solid #30363d; z-index: 99999; pointer-events: none; }
    </style>
    <div class="watermark">Created by iqbalmantam</div>
""",
    unsafe_allow_html=True,
)

st.title("🛡️ Background Check - OSINT Engine v4.0")
st.divider()

# Sidebar Input
with st.sidebar:
    st.header("📌 Input Identitas")
    email_in = st.text_input("Email Utama*", placeholder="contoh: kandidat@gmail.com")
    phone_in = st.text_input("Nomor HP (Indonesia)", placeholder="contoh: 08123456789")
    username_in = st.text_input("Username / Handle Medsos")
    name_in = st.text_input("Nama Lengkap Kandidat", placeholder="contoh: Iqbal Mantam")
    btn_submit = st.button("🚀 Jalankan Investigasi", type="primary", use_container_width=True)
    mask_sensitive = st.checkbox("🔒 Masking Data Sensitif", value=False)

def mask_text(text, type_mode="email"):
    if not text or not mask_sensitive: return text
    if type_mode == "email" and "@" in text:
        parts = text.split("@")
        return parts[0][:2] + "****@" + parts[1]
    return text

if btn_submit:
    if not email_in:
        st.error("⚠️ Email Utama Wajib Diisi!")
    else:
        # Penanganan jika nomor HP kosong
        clean_phone = phone_in if phone_in else "08000000000"
        
        # Proses Investigasi
        phone_data = analyze_indonesia_phone(clean_phone)
        telecom_links = generate_telecom_dorks(phone_data["intl_format"])
        identity_res = asyncio.run(check_email_identity(email_in))
        social_res = asyncio.run(check_indonesia_socials(username_in if username_in else name_in))
        breach_res = asyncio.run(check_data_breach(email_in))
        dorks = generate_indonesia_dorks(email_in, phone_data, username_in, name_in, "", "")
        
        st.session_state["results"] = {
            "name": name_in, "email": email_in, "phone": phone_data, "social": social_res, 
            "identity": identity_res, "breach": breach_res, "dorks": dorks, "telecom": telecom_links
        }
        st.rerun()

if "results" in st.session_state:
    res = st.session_state["results"]
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📱 Telecom & ID", "🌐 Social Matrix", "🎓 PDDikti Academic", "⚠️ Leak Intelligence", "⚖️ Legal & Export"])

    with tab1:
        st.subheader("Analytics Seluler")
        st.write(f"**Provider:** {res['phone']['provider']}")
        st.markdown(f"* 💬 [Live Chat WhatsApp]({res['phone']['wa_link']})")
        st.markdown(f"* 📇 [Direct Portal GetContact]({res['telecom']['getcontact']})")

    with tab2:
        if res['social']:
            st.dataframe(pd.DataFrame(res['social']), use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("🎓 PDDikti Academic Footprint")
        search_url = f"https://pddikti.kemdikbud.go.id/search/{quote_plus(res['name'])}" if res['name'] else "https://pddikti.kemdikbud.go.id"
        st.markdown(f"👉 **[Klik di sini untuk mencari '{res['name'] or res['email']}' di Portal Resmi PDDikti]({search_url})**")
        st.info("Pencarian akademik diarahkan langsung ke portal resmi untuk hasil yang akurat.")

    with tab4:
        if res['breach'].get("breached"):
            st.error("⚠️ Email terdeteksi dalam kebocoran data!")
            st.json(res['breach'].get("data"))
        else:
            st.success("✅ Email bersih.")

    with tab5:
        for d in res['dorks']:
            st.markdown(f"##### {d['title']}")
            st.code(d['query'])
            st.markdown(f"[👉 Eksekusi Pencarian]({d['link']})")
