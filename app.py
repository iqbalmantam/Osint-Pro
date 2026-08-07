import asyncio
import json
import streamlit as st
import pandas as pd
from modules.breach_checker import check_data_breach
from modules.dork_indonesia import generate_indonesia_dorks, generate_telecom_dorks
from modules.identity_osint import check_email_identity
from modules.indo_telecom import analyze_indonesia_phone
from modules.social_osint import check_indonesia_socials
from modules.osint_utils import generate_username_variations

st.set_page_config(page_title="OSINT Engine Pro v4.0", layout="wide")

# UI Enhancement: Custom Risk Engine Branding
st.markdown("""<style>
    .risk-score { font-size: 40px; font-weight: bold; text-align: center; }
    .stButton>button { border-radius: 10px; }
</style>""", unsafe_allow_html=True)

st.title("🛡️ OSINT Engine Pro v4.0")

with st.sidebar:
    st.header("📌 Input Identitas")
    email_in = st.text_input("Email Utama*")
    phone_in = st.text_input("Nomor HP*")
    name_in = st.text_input("Nama Lengkap")
    uploaded_file = st.file_uploader("📂 Unggah Foto Kandidat (Visual Search)", type=['jpg', 'png'])
    
    with st.expander("⚙️ Advanced Settings"):
        city_in = st.text_input("Domisili")
        company_in = st.text_input("Perusahaan Terakhir")
    
    btn_submit = st.button("🚀 Jalankan Investigasi Mendalam")

if btn_submit:
    # 1. Processing Logic
    phone_data = analyze_indonesia_phone(phone_in)
    identity_res = asyncio.run(check_email_identity(email_in))
    
    # 2. Username Variations for Social Matrix
    variations = generate_username_variations(name_in)
    # Jalankan pengecekan untuk variasi utama
    social_res = asyncio.run(check_indonesia_socials(variations[0])) 
    
    breach_res = asyncio.run(check_data_breach(email_in))
    
    # 3. Dynamic Risk Scoring
    risk_score = 100
    risk_notes = []
    if breach_res.get("breached"): risk_score -= 30; risk_notes.append("Data Breach Detected")
    if not identity_res.get("github", {}).get("found"): risk_score -= 20; risk_notes.append("Low Developer Footprint")
    
    st.session_state["results"] = {
        "score": risk_score, "notes": risk_notes, "phone": phone_data,
        "identity": identity_res, "social": social_res, "breach": breach_res
    }
    st.rerun()

# Dashboard View
if "results" in st.session_state:
    res = st.session_state["results"]
    
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(f"<div class='risk-score'>{res['score']}</div>", unsafe_allow_html=True)
        st.write(f"**Risk Level:** {'High' if res['score'] < 60 else 'Low'}")
    
    with c2:
        for note in res['notes']: st.warning(note)

    # Visual Search Tab (Optimized with Upload)
    if uploaded_file:
        st.image(uploaded_file, width=150, caption="Foto Kandidat Terunggah")
        st.info("Gunakan link ini untuk Google Lens: [Cari via Gambar](https://lens.google.com/uploadbyurl?url=https://your-server-url/path-to-image)")
