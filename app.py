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
    .risk-score { font-size: 36px; font-weight: bold; text-align: center; }
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
    elif type_mode == "phone" and len(text) > 6:
        return text[:4] + "****" + text[-3:]
    return text

if btn_submit:
    if not email_in:
        st.error("⚠️ Email Utama Wajib Diisi!")
    else:
        clean_phone = phone_in if phone_in else "08000000000"
        
        # Proses Modul OSINT Lengkap
        phone_data = analyze_indonesia_phone(clean_phone)
        telecom_links = generate_telecom_dorks(phone_data["intl_format"])
        identity_res = asyncio.run(check_email_identity(email_in))
        
        target_social = username_in if username_in else name_in
        social_res = asyncio.run(check_indonesia_socials(target_social)) if target_social else []
        
        breach_res = asyncio.run(check_data_breach(email_in))
        dorks = generate_indonesia_dorks(email_in, phone_data, username_in, name_in, "", "")
        
        # Risk Scoring
        risk_score = 100
        risk_notes = []
        if breach_res.get("breached"):
            risk_score -= 30
            risk_notes.append("Email terdeteksi dalam insiden Data Breach.")
        if not identity_res.get("github", {}).get("found") and not identity_res.get("gravatar", {}).get("found"):
            risk_score -= 15
            risk_notes.append("Jejak akun developer / gravatar publik rendah.")
            
        st.session_state["results"] = {
            "name": name_in, "email": email_in, "phone": phone_data, "social": social_res, 
            "identity": identity_res, "breach": breach_res, "dorks": dorks, "telecom": telecom_links,
            "score": risk_score, "notes": risk_notes
        }
        st.rerun()

if "results" in st.session_state:
    res = st.session_state["results"]
    
    # Summary Risk Assessment Box
    c_r1, c_r2 = st.columns([1, 3])
    with c_r1:
        st.markdown(f"<div class='risk-score'>{res['score']}/100</div>", unsafe_allow_html=True)
        st.write(f"**Risk Status:** {'High Risk' if res['score'] < 60 else 'Low/Medium Risk'}")
    with c_r2:
        st.write("**Catatan Evaluasi Risiko:**")
        if res['notes']:
            for note in res['notes']: st.warning(note)
        else:
            st.success("Tidak ada indikator risiko mayor yang ditemukan.")
            
    st.divider()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📱 Telecom & Identity", 
        "🌐 Social Matrix", 
        "🎓 PDDikti Academic", 
        "🔎 Visual Search",
        "⚠️ Leak Intelligence", 
        "⚖️ Legal & Export"
    ])

    with tab1:
        st.subheader("Analytics Seluler & Network Lookup")
        col_t1, col_t2, col_t3 = st.columns(3)
        col_t1.metric("Provider Seluler", res["phone"]["provider"])
        col_t2.metric("Format Lokal", mask_text(res["phone"]["local_format"], "phone"))
        col_t3.metric("Format Internasional", mask_text(res["phone"]["intl_format"], "phone"))

        st.markdown(f"* 💬 [Buka Live Chat WhatsApp]({res['phone']['wa_link']})")
        st.markdown(f"* ✈️ [Cek Profil Telegram]({res['phone']['telegram_link']})")
        st.markdown(f"* 📇 [Direct Web Portal GetContact]({res['telecom']['getcontact']})")
        
        st.divider()
        st.subheader(f"Identitas Terikat Email ({mask_text(res['email'], 'email')})")
        c_i1, c_i2 = st.columns(2)
        with c_i1:
            st.markdown("#### Gravatar / WordPress")
            g = res["identity"].get("gravatar", {})
            if g.get("found"):
                st.success("TERDAFTAR")
                if g.get("avatar"): st.image(g["avatar"], width=80)
                st.write(f"**Nama:** {g.get('display_name')}")
                st.markdown(f"[🔗 Buka Profil]({g.get('profile_url')})")
            else:
                st.info("Tidak terdaftar di Gravatar.")
        with c_i2:
            st.markdown("#### GitHub Footprint")
            gh = res["identity"].get("github", {})
            if gh.get("found"):
                st.success("TERDAFTAR")
                if gh.get("avatar"): st.image(gh["avatar"], width=80)
                st.write(f"**Username:** @{gh.get('username')}")
                st.markdown(f"[🔗 Buka GitHub]({gh.get('profile_url')})")
            else:
                st.info("Tidak terikat GitHub publik.")

    with tab2:
        st.subheader("Matrix Media Sosial")
        if res.get('social'):
            df_s = pd.DataFrame(res['social'])
            st.dataframe(df_s[["platform", "status_check", "direct_url", "dork_url"]], use_container_width=True, hide_index=True)
        else:
            st.info("Masukkan Username atau Nama untuk memindai media sosial.")

    with tab3:
        st.subheader("🎓 PDDikti Academic Footprint")
        search_url = f"https://pddikti.kemdikbud.go.id/search/{quote_plus(res['name'])}" if res['name'] else "https://pddikti.kemdikbud.go.id"
        st.markdown(f"👉 **[Klik di sini untuk mencari '{res['name'] or res['email']}' di Portal Resmi PDDikti]({search_url})**")
        st.info("Pencarian akademik diarahkan langsung ke portal resmi untuk hasil yang akurat.")

    with tab4:
        st.subheader("Reverse Image Search")
        avatar_url = res["identity"].get("gravatar", {}).get("avatar") or res["identity"].get("github", {}).get("avatar")
        if avatar_url:
            st.image(avatar_url, width=120, caption="Avatar Terdeteksi")
            lens_url = f"https://lens.google.com/uploadbyurl?url={quote_plus(avatar_url)}"
            st.markdown(f"[🔍 Lacak via Google Lens]({lens_url})")
        else:
            st.info("Tidak ada foto profil otomatis yang terdeteksi.")

    with tab5:
        st.subheader("Data Leakage Check")
        if res['breach'].get("breached"):
            st.error("⚠️ Email terdeteksi dalam kebocoran data!")
            st.json(res['breach'].get("data"))
        else:
            st.success("✅ Email bersih dari database kebocoran publik utama.")

    with tab6:
        st.subheader("Legal Dorking & Report Export")
        for d in res['dorks']:
            st.markdown(f"##### {d['title']}")
            st.code(d['query'])
            st.markdown(f"[👉 Eksekusi Pencarian]({d['link']})")
