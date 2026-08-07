import asyncio
import json
import time
import streamlit as st
import pandas as pd
from modules.breach_checker import check_data_breach
from modules.dork_indonesia import generate_indonesia_dorks, generate_telecom_dorks
from modules.identity_osint import check_email_identity
from modules.indo_telecom import analyze_indonesia_phone
from modules.social_osint import check_indonesia_socials
from modules.osint_utils import generate_username_variations

st.set_page_config(page_title="OSINT Engine Pro v4.0", layout="wide")

# Custom CSS UI & Privacy Watermark
st.markdown("""<style>
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    .risk-score { font-size: 40px; font-weight: bold; text-align: center; }
    .stButton>button { border-radius: 10px; }
    .watermark { position: fixed; bottom: 15px; left: 50%; transform: translateX(-50%); opacity: 0.85; font-size: 13px; font-weight: 600; color: #8b949e; background-color: rgba(22, 27, 34, 0.9); padding: 6px 18px; border-radius: 20px; border: 1px solid #30363d; z-index: 99999; }
</style>
<div class="watermark">Created by iqbalmantam</div>""", unsafe_allow_html=True)

st.title("🛡️ OSINT Engine Pro v4.0")
st.caption("Enterprise Candidate Investigation & Verification Platform")
st.divider()

with st.sidebar:
    st.header("📌 Input Identitas")
    email_in = st.text_input("Email Utama*", placeholder="contoh: kandidat@gmail.com")
    phone_in = st.text_input("Nomor HP*", placeholder="contoh: 08123456789")
    username_in = st.text_input("Username / Handle Medsos", placeholder="opsional")
    name_in = st.text_input("Nama Lengkap", placeholder="contoh: Budi Santoso")
    uploaded_file = st.file_uploader("📂 Unggah Foto Kandidat (Visual Search)", type=['jpg', 'png'])
    
    with st.expander("⚙️ Advanced Settings"):
        city_in = st.text_input("Domisili")
        company_in = st.text_input("Perusahaan Terakhir")
    
    btn_submit = st.button("🚀 Jalankan Investigasi Mendalam", type="primary", use_container_width=True)

if btn_submit:
    if not email_in or not phone_in:
        st.error("⚠️ Email dan Nomor HP Wajib Diisi!")
    else:
        progress_bar = st.progress(0, text="Menginisialisasi...")
        
        phone_data = analyze_indonesia_phone(phone_in)
        telecom_links = generate_telecom_dorks(phone_data["intl_format"])
        time.sleep(0.1)
        
        identity_res = asyncio.run(check_email_identity(email_in))
        time.sleep(0.1)
        
        target_social = username_in.strip() if username_in else ""
        if not target_social and name_in:
            target_social = name_in.strip()
            
        social_res = asyncio.run(check_indonesia_socials(target_social)) if target_social else []
        time.sleep(0.1)
        
        breach_res = asyncio.run(check_data_breach(email_in))
        dorks = generate_indonesia_dorks(email_in, phone_data, username_in, name_in, city_in, company_in)
        
        # Dynamic Risk Scoring
        risk_score = 100
        risk_notes = []
        if breach_res.get("breached"): 
            risk_score -= 30
            risk_notes.append("Data Breach Detected (Email ditemukan dalam database kebocoran)")
        if not identity_res.get("github", {}).get("found") and not identity_res.get("gravatar", {}).get("found"): 
            risk_score -= 15
            risk_notes.append("Low Developer/Public Footprint")
            
        progress_bar.progress(100, text="Selesai!")
        time.sleep(0.3)
        progress_bar.empty()
        
        st.session_state["results"] = {
            "score": risk_score, "notes": risk_notes, "phone": phone_data,
            "identity": identity_res, "social": social_res, "breach": breach_res,
            "dorks": dorks, "telecom_links": telecom_links, "email": email_in
        }
        st.rerun()

# Dashboard View
if "results" in st.session_state:
    res = st.session_state["results"]
    
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(f"<div class='risk-score'>{res['score']}/100</div>", unsafe_allow_html=True)
        st.write(f"**Risk Level:** {'High Risk' if res['score'] < 60 else 'Low/Medium Risk'}")
    
    with c2:
        st.write("**Catatan Evaluasi Risk Engine:**")
        if res['notes']:
            for note in res['notes']: st.warning(note)
        else:
            st.success("Tidak ada indikator risiko mayor yang ditemukan.")

    st.divider()
    
    tab1, tab2, tab3, tab4 = st.tabs(["📱 Telecom & Socials", "⚠️ Leak Intelligence", "🔎 Visual Search", "⚖️ Dorking & Report"])
    
    with tab1:
        st.subheader("Analytics Kontak & Socials")
        st.write(f"**Provider:** {res['phone']['provider']}")
        st.write(f"**Format Lokal:** {res['phone']['local_format']}")
        
        if res.get('social'):
            st.write("---")
            st.write("**Daftar Tautan Pencarian Media Sosial (Klik untuk Membuka):**")
            
            for item in res['social']:
                col_a, col_b, col_c = st.columns([1.5, 2, 2.5])
                with col_a:
                    st.markdown(f"**{item.get('platform')}**")
                with col_b:
                    st.markdown(f"Status: `{item.get('status_check')}`")
                with col_c:
                    url = item.get('dork_url')
                    if url:
                        st.markdown(f"[🔗 Buka Tautan Pencarian]({url})", unsafe_allow_html=True)
                st.write("")
        else:
            st.info("Tidak ada target sosial media/username yang diproses.")
            
    with tab2:
        st.subheader("Data Leakage Check")
        if res['breach'].get("breached"):
            st.error("Email terdeteksi dalam kebocoran data!")
            st.json(res['breach'].get("data"))
        else:
            st.success("Email bersih dari database kebocoran data publik utama.")
            
    with tab3:
        st.subheader("Visual Search (Reverse Image)")
        if uploaded_file:
            st.image(uploaded_file, width=150, caption="Foto Kandidat")
            st.info("Catatan: Untuk melakukan pencarian langsung lewat URL gambar, unggah foto ke layanan hosting gambar publik (seperti Imgur) lalu gunakan link hasilnya.")
        else:
            st.info("Unggah foto pada panel sidebar untuk mengaktifkan opsi visual search.")
            
    with tab4:
        st.subheader("Legal Dorking Links")
        for d in res['dorks']:
            st.markdown(f"##### {d['title']}")
            st.code(d['query'], language="text")
            st.markdown(f"[Buka Link Dork]({d['link']})")
