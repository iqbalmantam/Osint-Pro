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

# Custom CSS UI
st.markdown(
    """
    <style>
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .watermark { position: fixed; bottom: 15px; left: 50%; transform: translateX(-50%); opacity: 0.85; font-size: 13px; font-weight: 600; color: #8b949e; background-color: rgba(22, 27, 34, 0.9); padding: 6px 18px; border-radius: 20px; border: 1px solid #30363d; z-index: 99999; }
    </style>
    <div class="watermark">Created by iqbalmantam</div>
""",
    unsafe_allow_html=True,
)

st.title("🛡️ Background Check - OSINT Engine v4.0")
st.divider()

# Sidebar
with st.sidebar:
    st.header("📌 Input Identitas Utama")
    email_in = st.text_input("Email Utama*", placeholder="contoh: kandidat@gmail.com")
    phone_in = st.text_input("Nomor HP (Indonesia)*", placeholder="contoh: 08123456789")
    username_in = st.text_input("Username / Handle Medsos", placeholder="contoh: iqbalmantam")
    name_in = st.text_input("Nama Lengkap Kandidat", placeholder="contoh: Budi Santoso")

    with st.expander("⚙️ Refinement Filters"):
        city_in = st.text_input("Kota / Domisili")
        company_in = st.text_input("Perusahaan Terakhir")

    btn_submit = st.button("🚀 Jalankan Investigasi", type="primary", use_container_width=True)
    mask_sensitive = st.checkbox("🔒 Masking Data Sensitif")

# Logika Investigasi (Tanpa PDDikti)
if btn_submit:
    if not email_in or not phone_in:
        st.error("⚠️ Email dan Nomor HP Wajib Diisi!")
    else:
        progress_bar = st.progress(0, text="Menginisialisasi...")
        
        phone_data = analyze_indonesia_phone(phone_in)
        telecom_links = generate_telecom_dorks(phone_data["intl_format"])
        
        identity_res = asyncio.run(check_email_identity(email_in))
        
        target_social_input = username_in if username_in else name_in
        social_res = asyncio.run(check_indonesia_socials(target_social_input)) if target_social_input else []
        
        breach_res = asyncio.run(check_data_breach(email_in))
        dorks = generate_indonesia_dorks(email_in, phone_data, username_in, name_in, city_in, company_in)
        
        # Risk Score Logic
        risk_score = 100
        risk_notes = []
        if breach_res.get("breached"): risk_score -= 30
        if not identity_res.get("github", {}).get("found") and not identity_res.get("gravatar", {}).get("found"): risk_score -= 15
        
        st.session_state["osint_results"] = {
            "email_in": email_in, "phone_data": phone_data, "username_in": username_in,
            "name_in": name_in, "identity_res": identity_res, "social_res": social_res,
            "breach_res": breach_res, "dorks": dorks, "telecom_links": telecom_links,
            "risk_score": risk_score, "risk_notes": risk_notes
        }
        st.rerun()

# Dashboard
if "osint_results" in st.session_state:
    res = st.session_state["osint_results"]
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📱 Telecom & Identity", "🌐 Social Matrix", "🔎 Visual Search", "⚠️ Leak Intelligence", "⚖️ Legal & Export"])
    
    with tab1: # (Isi tab 1 sama seperti sebelumnya)
        st.subheader("📱 Analytics Seluler")
        # ... (Tampilkan konten tab 1)
    with tab2:
        # ... (Tampilkan konten tab 2)
    with tab3: # (Tadinya PDDikti, sekarang Visual Search)
        # ... (Tampilkan konten Visual Search)
    with tab4:
        # ... (Tampilkan konten Leak Intelligence)
    with tab5:
        # ... (Tampilkan konten Legal & Export)
