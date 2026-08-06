import streamlit as st
import asyncio
import pandas as pd
from urllib.parse import quote_plus

from modules.indo_telecom import analyze_indonesia_phone
from modules.identity_osint import check_email_identity
from modules.social_osint import check_indonesia_socials
from modules.breach_checker import check_data_breach
from modules.dork_indonesia import generate_indonesia_dorks, generate_telecom_dorks

st.set_page_config(
    page_title="Background Check - OSINT Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Versi Stabil Awal
st.markdown("""
    <style>
    /* Sembunyikan menu bawaan & footer Streamlit */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header[data-testid="stHeader"] { visibility: hidden; }

    /* Watermark di tengah bawah */
    .watermark {
        position: fixed;
        bottom: 15px;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0.85;
        font-size: 13px;
        font-weight: 600;
        color: #8b949e;
        background-color: rgba(22, 27, 34, 0.9);
        padding: 6px 18px;
        border-radius: 20px;
        border: 1px solid #30363d;
        z-index: 99999;
        pointer-events: none;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    </style>
    
    <div class="watermark">Created by iqbalmantam</div>
""", unsafe_allow_html=True)

st.title("🛡️ Background Check - OSINT")
st.caption("Platform Background Check Kandidat (100% Real-Time & Live Connection)")
st.divider()

# Sidebar Input
with st.sidebar:
    st.header("📌 Input Identitas Kandidat")
    email_in = st.text_input("Email Utama*", placeholder="contoh: kandidat@gmail.com")
    phone_in = st.text_input("Nomor HP (Indonesia)*", placeholder="contoh: 08123456789 atau 62812...")
    username_in = st.text_input("Username / Handle Medsos", placeholder="contoh: iqbalmantam")
    name_in = st.text_input("Nama Lengkap Kandidat", placeholder="contoh: Budi Santoso")
    
    st.markdown("---")
    btn_submit = st.button("🚀 Jalankan Investigasi OSINT", type="primary", use_container_width=True)

    st.markdown("<br><br><div style='text-align: center; color: #8b949e; font-size: 12px;'>Engine OSINT v3.0<br><b>Created by iqbalmantam</b></div>", unsafe_allow_html=True)

# Proses Data saat Tombol Di-klik & Simpan ke Session State
if btn_submit:
    if not email_in or not phone_in:
        st.error("⚠️ Email dan Nomor HP Wajib Diisi sebagai Primary Anchor Key!")
    else:
        phone_data = analyze_indonesia_phone(phone_in)
        st.toast("Menghubungkan ke server jaringan publik secara real-time...", icon="🔄")
        
        # Async Executions
        identity_res = asyncio.run(check_email_identity(email_in))
        
        target_social_input = username_in if username_in else name_in
        social_res = asyncio.run(check_indonesia_socials(target_social_input)) if target_social_input else []
        
        breach_res = asyncio.run(check_data_breach(email_in))
        dorks = generate_indonesia_dorks(email_in, phone_data, username_in, name_in)
        telecom_links = generate_telecom_dorks(phone_data["intl_format"])

        # Risk Scoring Engine
        active_social_count = len([s for s in social_res if s.get("status_check") == "🟢 Terverifikasi Ada"]) if social_res else 0
        has_github = identity_res.get("github", {}).get("found", False)
        has_gravatar = identity_res.get("gravatar", {}).get("found", False)
        is_breached = breach_res.get("breached", False)

        risk_score = 100
        risk_notes = []

        if is_breached:
            risk_score -= 30
            risk_notes.append("Email terdeteksi pernah terkena insiden Kebocoran Data (Data Breach).")
        if not has_github and not has_gravatar:
            risk_score -= 20
            risk_notes.append("Tidak ditemukan jejak identitas developer/WordPress publik.")
        if active_social_count == 0 and target_social_input:
            risk_score -= 20
            risk_notes.append("Username/Nama yang dimasukkan tidak menghasilkan jejak dorking terdeteksi.")

        # Simpan Seluruh Hasil ke Session State
        st.session_state["osint_results"] = {
            "email_in": email_in,
            "phone_data": phone_data,
            "username_in": username_in,
            "name_in": name_in,
            "identity_res": identity_res,
            "social_res": social_res,
            "breach_res": breach_res,
            "dorks": dorks,
            "telecom_links": telecom_links,
            "risk_score": risk_score,
            "risk_notes": risk_notes,
            "is_breached": is_breached
        }

# Menampilkan Hasil Investigasi dari Session State (Tetap Bertahan Setelah Download)
if "osint_results" in st.session_state:
    res = st.session_state["osint_results"]
    
    # Risk Banner
    st.subheader("📊 Summary & Digital Footprint Risk Score")
    col_risk1, col_risk2 = st.columns([1, 2])
    
    with col_risk1:
        if res["risk_score"] >= 80:
            st.success(f"### Score: {res['risk_score']}/100 (LOW RISK)")
        elif res["risk_score"] >= 50:
            st.warning(f"### Score: {res['risk_score']}/100 (MEDIUM RISK)")
        else:
            st.error(f"### Score: {res['risk_score']}/100 (HIGH RISK)")
            
    with col_risk2:
        st.write("**Catatan Evaluasi Otomatis:**")
        if res["risk_notes"]:
            for note in res["risk_notes"]:
                st.write(f"- ⚠️ {note}")
        else:
            st.write("- ✅ Jejak digital kandidat konsisten dan terakreditasi baik.")

    st.divider()

    # UI Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📱 Telecom & Identity", 
        "🌐 Social Matrix", 
        "🔎 Reverse Image Search",
        "⚠️ Leak Intelligence",
        "⚖️ Legal Dorking & Report"
    ])

    # TAB 1: Telecom & Identity
    with tab1:
        st.subheader("📱 Analytics Seluler & Tags Lookup")
        col_tel1, col_tel2, col_tel3 = st.columns(3)
        col_tel1.metric("Provider Seluler", res["phone_data"]["provider"])
        col_tel2.metric("Format Lokal", res["phone_data"]["local_format"])
        col_tel3.metric("Format Internasional", res["phone_data"]["intl_format"])
        
        st.markdown(f"* 💬 [Buka Live Chat WhatsApp Kandidat]({res['phone_data']['wa_link']})")
        st.markdown(f"* ✈️ [Cek Profil Telegram via Phone Number]({res['phone_data']['telegram_link']})")
        st.markdown(f"* 📞 [Pindai Tags/Nama Kontak via Truecaller]({res['telecom_links']['truecaller']})")
        st.markdown(f"* 📇 [Akses GetContact Web Portal]({res['telecom_links']['getcontact']})")
        
        st.divider()
        
        st.subheader("👤 Identitas Utama Terikat Email")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### Gravatar / WordPress Global")
            g = res["identity_res"].get("gravatar", {})
            if g.get("found"):
                st.success("AKUN AKTIF TERDAFTAR")
                if g.get("avatar"): st.image(g["avatar"], width=80)
                st.write(f"**Nama Display:** {g.get('display_name')}")
                st.write(f"**Bio:** {g.get('about')}")
                st.markdown(f"[🔗 Buka Profil Gravatar]({g.get('profile_url')})")
            else:
                st.info("Tidak terdaftar di Gravatar.")

        with c2:
            st.markdown("#### GitHub Developer Footprint")
            gh = res["identity_res"].get("github", {})
            if gh.get("found"):
                st.success("AKUN AKTIF TERDAFTAR")
                if gh.get("avatar"): st.image(gh["avatar"], width=80)
                st.write(f"**Username:** @{gh.get('username')}")
                st.write(f"**Public Repos:** {gh.get('repos')}")
                st.write(f"**Bio / Perusahaan:** {gh.get('bio')} | {gh.get('company')}")
                st.markdown(f"[🔗 Buka Repositori GitHub]({gh.get('profile_url')})")
            else:
                st.info("Email tidak terikat GitHub publik.")

    # TAB 2: Social Matrix (Auto Cross-Check & Dorking Search)
    with tab2:
        st.subheader("🌐 Matrix Media Sosial (Auto Cross-Check & Dorking)")
        st.caption("Sistem memverifikasi status ketersediaan profil secara otomatis di latar belakang.")
        
        if res.get("social_res"):
            df_s = pd.DataFrame(res["social_res"])
            
            # Pastikan kolom wajib ada (menghindari KeyError jika session_state menggunakan data lama)
            expected_cols = ["platform", "status_check", "direct_url", "dork_url"]
            for col in expected_cols:
                if col not in df_s.columns:
                    df_s[col] = "🟡 Perlu Diulas Manual" if col == "status_check" else "#"

            st.dataframe(
                df_s[expected_cols], 
                column_config={
                    "platform": "Platform Target",
                    "status_check": "Verifikasi Otomatis",
                    "direct_url": st.column_config.LinkColumn("Buka Direct Profil"),
                    "dork_url": st.column_config.LinkColumn("Verifikasi via Google Dork")
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Masukkan Username atau Nama Kandidat di sidebar untuk memunculkan tautan pencarian.")

    # TAB 3: REVERSE IMAGE SEARCH ENGINE
    with tab3:
        st.subheader("🖼️ Reverse Image Search Engine")
        st.write("Analisis foto kandidat ke berbagai mesin pencari visual untuk mendeteksi keaslian profil:")
        
        avatar_url = res["identity_res"].get("gravatar", {}).get("avatar") or res["identity_res"].get("github", {}).get("avatar")
        
        if avatar_url:
            st.image(avatar_url, caption="Foto Profil Terdeteksi", width=120)
            lens_url = f"https://lens.google.com/uploadbyurl?url={quote_plus(avatar_url)}"
            yandex_url = f"https://yandex.com/images/search?rpt=imageview&url={quote_plus(avatar_url)}"
            tineye_url = f"https://tineye.com/search?url={quote_plus(avatar_url)}"
            
            col_img1, col_img2, col_img3 = st.columns(3)
            col_img1.markdown(f"[🔍 Lacak via Google Lens]({lens_url})")
            col_img2.markdown(f"[🔍 Lacak via Yandex Visual]({yandex_url})")
            col_img3.markdown(f"[🔍 Lacak via TinEye Search]({tineye_url})")
        else:
            st.info("Foto profil otomatis dari Gravatar/GitHub tidak ditemukan. Kamu bisa memasukkan URL foto kandidat secara manual di bawah ini:")
            manual_img = st.text_input("URL Foto Kandidat (PNG/JPG):", placeholder="https://domain.com/foto.jpg")
            if manual_img:
                lens_url = f"https://lens.google.com/uploadbyurl?url={quote_plus(manual_img)}"
                yandex_url = f"https://yandex.com/images/search?rpt=imageview&url={quote_plus(manual_img)}"
                st.markdown(f"* [🔍 Lacak Foto Manual di Google Lens]({lens_url})")
                st.markdown(f"* [🔍 Lacak Foto Manual di Yandex Visual]({yandex_url})")

    # TAB 4: Leak Intelligence
    with tab4:
        st.subheader("⚠️ Data Leakage Check")
        if res["breach_res"].get("breached"):
            st.error("⚠️ WARN: Email ini ditemukan dalam insiden kebocoran data publik!")
            st.json(res["breach_res"].get("data"))
        else:
            st.success("✅ Email ini bersih dan tidak terdeteksi dalam insiden kebocoran data publik besar.")

    # TAB 5: Legal Dorking & Report Download
    with tab5:
        st.subheader("⚖️ Legal & Court Precision Search")
        for d in res["dorks"]:
            st.markdown(f"##### {d['title']}")
            st.code(d["query"], language="text")
            st.markdown(f"[👉 Eksekusi Pencarian Langsung di Google]({d['link']})")
            st.write("")
            
        st.divider()
        
        # EXPORT REPORT (TUNGGAL: PRINTABLE HTML)
        st.subheader("📥 Export Audit Report")
        
        html_report = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OSINT Audit Report - {res['name_in'] or res['email_in']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 24px; color: #1e293b; background-color: #ffffff; }}
                h1 {{ color: #0f172a; border-bottom: 2px solid #3b82f6; padding-bottom: 8px; margin-bottom: 20px; }}
                .section {{ margin-bottom: 20px; padding: 16px; border: 1px solid #e2e8f0; border-radius: 8px; background-color: #f8fafc; }}
                .score {{ font-weight: bold; font-size: 20px; color: {'#16a34a' if res['risk_score']>=80 else '#dc2626'}; }}
                .footer {{ margin-top: 40px; font-size: 11px; text-align: center; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 12px; }}
            </style>
        </head>
        <body>
            <h1>🛡️ OSINT Executive Candidate Report</h1>
            <div class="section">
                <p><b>Nama Kandidat:</b> {res['name_in'] or 'N/A'}</p>
                <p><b>Email Utama:</b> {res['email_in']}</p>
                <p><b>Nomor Kontak:</b> {res['phone_data']['local_format']} ({res['phone_data']['provider']})</p>
                <p><b>Timestamp Audit:</b> {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} WIB</p>
                <p><b>Risk Score:</b> <span class="score">{res['risk_score']} / 100</span></p>
            </div>
            <div class="section">
                <h3>Temuan & Catatan Audit:</h3>
                <ul>
                    {''.join([f'<li>{n}</li>' for n in res['risk_notes']]) if res['risk_notes'] else '<li>Tidak ada temuan berisiko. Rekam jejak digital terindikasi baik.</li>'}
                </ul>
            </div>
            <div class="footer">
                Generated by Candidate OSINT Intelligence Engine • Created by iqbalmantam
            </div>
        </body>
        </html>
        """
        
        st.download_button(
            label="📥 Download Printable Report (.HTML)",
            data=html_report,
            file_name=f"OSINT_Report_{res['email_in'].split('@')[0]}.html",
            mime="text/html",
            use_container_width=True
        )
