import streamlit as st
import asyncio
import time
import pandas as pd
import json
from urllib.parse import quote_plus

from modules.indo_telecom import analyze_indonesia_phone
from modules.identity_osint import check_email_identity
from modules.social_osint import check_indonesia_socials
from modules.breach_checker import check_data_breach
from modules.dork_indonesia import generate_indonesia_dorks, generate_telecom_dorks
from modules.pddikti_osint import generate_pddikti_dorks

st.set_page_config(
    page_title="Background Check - OSINT Engine v4.0",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    div[data-testid="stToolbarActions"],
    header[data-testid="stHeader"] .stActionButton,
    header[data-testid="stHeader"] a[href*="github.com"] {
        display: none !important;
        visibility: hidden !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    [data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

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
    
    @media print {
        header, .stSidebar, .watermark, button { display: none !important; }
    }
    </style>
    
    <div class="watermark">Created by iqbalmantam</div>
""", unsafe_allow_html=True)

st.title("🛡️ Background Check - OSINT Engine v4.0")
st.caption("Enterprise Candidate Investigation & Verification Platform (Real-Time Live Connection)")
st.divider()

# Sidebar Input & Filters
with st.sidebar:
    st.header("📌 Input Identitas Utama")
    email_in = st.text_input("Email Utama*", placeholder="contoh: kandidat@gmail.com")
    phone_in = st.text_input("Nomor HP (Indonesia)*", placeholder="contoh: 08123456789")
    username_in = st.text_input("Username / Handle Medsos", placeholder="contoh: iqbalmantam")
    name_in = st.text_input("Nama Lengkap Kandidat", placeholder="contoh: Budi Santoso")
    
    with st.expander("⚙️ Refinement Filters (Opsional)"):
        city_in = st.text_input("Kota / Domisili", placeholder="contoh: Jakarta")
        company_in = st.text_input("Perusahaan / Kampus Terakhir", placeholder="contoh: PT Maju Jaya")

    st.markdown("---")
    
    col_b1, col_b2 = st.columns([3, 1])
    with col_b1:
        btn_submit = st.button("🚀 Jalankan Investigasi", type="primary", use_container_width=True)
    with col_b2:
        if st.button("🔄", help="Reset Data Session"):
            st.session_state.clear()
            st.rerun()

    mask_sensitive = st.checkbox("🔒 Masking Data Sensitif", value=False, help="Sensor nomor telepon dan email pada tampilan dashboard")
    st.markdown("<br><div style='text-align: center; color: #8b949e; font-size: 12px;'>OSINT Engine Enterprise v4.0<br><b>Created by iqbalmantam</b></div>", unsafe_allow_html=True)

def mask_text(text, type_mode="email"):
    if not text or not mask_sensitive:
        return text
    if type_mode == "email" and "@" in text:
        parts = text.split("@")
        return parts[0][:2] + "****@" + parts[1]
    elif type_mode == "phone" and len(text) > 6:
        return text[:4] + "****" + text[-3:]
    return text

if btn_submit:
    if not email_in or not phone_in:
        st.error("⚠️ Email dan Nomor HP Wajib Diisi sebagai Primary Key!")
    else:
        progress_bar = st.progress(0, text="Menginisialisasi Engine Investigasi OSINT...")
        
        progress_bar.progress(15, text="📱 Menguraikan Provider Seluler & Format Kontak...")
        phone_data = analyze_indonesia_phone(phone_in)
        telecom_links = generate_telecom_dorks(phone_data["intl_format"])
        time.sleep(0.2)
        
        progress_bar.progress(35, text="👤 Melacak Identitas Utama (Gravatar & GitHub)...")
        identity_res = asyncio.run(check_email_identity(email_in))
        time.sleep(0.2)
        
        progress_bar.progress(60, text="🌐 Memverifikasi Ketersediaan Media Sosial...")
        target_social_input = username_in if username_in else name_in
        social_res = asyncio.run(check_indonesia_socials(target_social_input)) if target_social_input else []
        time.sleep(0.2)
        
        progress_bar.progress(80, text="⚠️ Memeriksa Kebocoran Data & Rekam Akademik (PDDikti)...")
        breach_res = asyncio.run(check_data_breach(email_in))
        dorks = generate_indonesia_dorks(email_in, phone_data, username_in, name_in, city_in, company_in)
        pddikti_dorks = generate_pddikti_dorks(name_in, company_in or city_in)
        time.sleep(0.2)
        
        progress_bar.progress(95, text="📊 Menghitung Dynamic Risk Score...")
        active_social_count = len([s for s in social_res if s.get("status_check") == "🟢 Terverifikasi Ada"]) if social_res else 0
        has_github = identity_res.get("github", {}).get("found", False)
        has_gravatar = identity_res.get("gravatar", {}).get("found", False)
        is_breached = breach_res.get("breached", False)

        risk_score = 100
        risk_notes = []

        if is_breached:
            risk_score -= 30
            risk_notes.append("Email terdeteksi dalam insiden Kebocoran Data (Data Breach).")
        if not has_github and not has_gravatar:
            risk_score -= 15
            risk_notes.append("Tidak ditemukan jejak akun developer/WordPress publik.")
        if active_social_count == 0 and target_social_input:
            risk_score -= 15
            risk_notes.append("Username/Nama tidak menghasilkan media sosial aktif yang terverifikasi.")

        progress_bar.progress(100, text="✅ Investigasi OSINT Selesai!")
        time.sleep(0.4)
        progress_bar.empty()

        st.session_state["osint_results"] = {
            "email_in": email_in,
            "phone_data": phone_data,
            "username_in": username_in,
            "name_in": name_in,
            "city_in": city_in,
            "company_in": company_in,
            "identity_res": identity_res,
            "social_res": social_res,
            "breach_res": breach_res,
            "dorks": dorks,
            "pddikti_dorks": pddikti_dorks,
            "telecom_links": telecom_links,
            "risk_score": risk_score,
            "risk_notes": risk_notes,
            "is_breached": is_breached
        }

if "osint_results" in st.session_state:
    res = st.session_state["osint_results"]
    
    st.subheader("📊 Summary & Digital Risk Assessment")
    c_risk1, c_risk2 = st.columns([1, 2])
    
    with c_risk1:
        if res["risk_score"] >= 80:
            st.success(f"### Score: {res['risk_score']}/100 (LOW RISK)")
        elif res["risk_score"] >= 50:
            st.warning(f"### Score: {res['risk_score']}/100 (MEDIUM RISK)")
        else:
            st.error(f"### Score: {res['risk_score']}/100 (HIGH RISK)")
            
    with c_risk2:
        st.write("**Catatan Evaluasi Risk Engine:**")
        if res["risk_notes"]:
            for note in res["risk_notes"]:
                st.write(f"- ⚠️ {note}")
        else:
            st.write("- ✅ Rekam jejak digital terindikasi konsisten dan berisiko rendah.")

    st.divider()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📱 Telecom & Identity", 
        "🌐 Social Matrix", 
        "🎓 Akademik & PDDikti",
        "🔎 Visual Search",
        "⚠️ Leak Intelligence",
        "⚖️ Legal & Export"
    ])

    with tab1:
        st.subheader("📱 Analytics Seluler & Network Lookup")
        col_t1, col_t2, col_t3 = st.columns(3)
        col_t1.metric("Provider Seluler", res["phone_data"]["provider"])
        col_t2.metric("Format Lokal", mask_text(res["phone_data"]["local_format"], "phone"))
        col_t3.metric("Format Internasional", mask_text(res["phone_data"]["intl_format"], "phone"))
        
        st.markdown(f"* 💬 [Buka Live Chat WhatsApp Kandidat]({res['phone_data']['wa_link']})")
        st.markdown(f"* ✈️ [Cek Profil Telegram via Phone Number]({res['phone_data']['telegram_link']})")
        st.markdown(f"* 📞 [Pindai Nama Kontak via Truecaller (Perlu Login)]({res['telecom_links']['truecaller']})")
        st.markdown(f"* 📇 [Cek Indeks Tags GetContact via Google Dork]({res['telecom_links']['getcontact']})")
        
        st.divider()
        st.subheader("👤 Identitas Terikat Email (" + mask_text(res['email_in'], 'email') + ")")
        c_i1, c_i2 = st.columns(2)
        
        with c_i1:
            st.markdown("#### Gravatar / WordPress Global")
            g = res["identity_res"].get("gravatar", {})
            if g.get("found"):
                st.success("AKUN TERDAFTAR")
                if g.get("avatar"): st.image(g["avatar"], width=80)
                st.write(f"**Nama Display:** {g.get('display_name')}")
                st.write(f"**Bio:** {g.get('about')}")
                st.markdown(f"[🔗 Buka Profil Gravatar]({g.get('profile_url')})")
            else:
                st.info("Tidak terdaftar di Gravatar.")

        with c_i2:
            st.markdown("#### GitHub Developer Footprint")
            gh = res["identity_res"].get("github", {})
            if gh.get("found"):
                st.success("AKUN TERDAFTAR")
                if gh.get("avatar"): st.image(gh["avatar"], width=80)
                st.write(f"**Username:** @{gh.get('username')}")
                st.write(f"**Public Repos:** {gh.get('repos')}")
                st.markdown(f"[🔗 Buka Repositori GitHub]({gh.get('profile_url')})")
            else:
                st.info("Email tidak terikat GitHub publik.")

    with tab2:
        st.subheader("🌐 Matrix Media Sosial & Dorking")
        if res.get("social_res"):
            df_s = pd.DataFrame(res["social_res"])
            st.dataframe(
                df_s[["platform", "status_check", "direct_url", "dork_url"]], 
                column_config={
                    "platform": "Platform Target",
                    "status_check": "Verifikasi Status",
                    "direct_url": st.column_config.LinkColumn("Buka Profil Direct"),
                    "dork_url": st.column_config.LinkColumn("Buka Google Dork")
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Masukkan Username atau Nama untuk mengaktifkan matrix media sosial.")

    with tab3:
        st.subheader("🎓 Verifikasi Rekam Akademik & PDDikti")
        if res.get("pddikti_dorks"):
            for p in res["pddikti_dorks"]:
                st.markdown(f"##### {p['title']}")
                st.code(p["query"], language="text")
                st.markdown(f"[👉 Eksekusi Pencarian di Google]({p['link']})")
                st.write("")
        else:
            st.info("Masukkan Nama Lengkap Kandidat untuk mengaktifkan pencarian PDDikti.")

    with tab4:
        st.subheader("🖼️ Reverse Image Search Engine")
        avatar_url = res["identity_res"].get("gravatar", {}).get("avatar") or res["identity_res"].get("github", {}).get("avatar")
        
        if avatar_url:
            st.image(avatar_url, caption="Foto Profil Terdeteksi", width=120)
            lens_url = f"https://lens.google.com/uploadbyurl?url={quote_plus(avatar_url)}"
            yandex_url = f"https://yandex.com/images/search?rpt=imageview&url={quote_plus(avatar_url)}"
            
            c_v1, c_v2 = st.columns(2)
            c_v1.markdown(f"[🔍 Lacak via Google Lens]({lens_url})")
            c_v2.markdown(f"[🔍 Lacak via Yandex Visual]({yandex_url})")
        else:
            st.info("Masukkan URL foto kandidat secara manual untuk melacak sumber visual:")
            manual_img = st.text_input("URL Foto Kandidat (PNG/JPG):", placeholder="https://domain.com/foto.jpg")
            if manual_img:
                lens_url = f"https://lens.google.com/uploadbyurl?url={quote_plus(manual_img)}"
                st.markdown(f"* [🔍 Lacak Foto Manual di Google Lens]({lens_url})")

    with tab5:
        st.subheader("⚠️ Data Leakage Check")
        if res["breach_res"].get("breached"):
            st.error("⚠️ WARNING: Email ini ditemukan dalam insiden kebocoran data publik!")
            st.json(res["breach_res"].get("data"))
        else:
            st.success("✅ Email ini bersih dan tidak terdeteksi dalam insiden kebocoran data publik besar.")

    with tab6:
        st.subheader("⚖️ Legal Dorking & Report Multi-Format Export")
        for d in res["dorks"]:
            st.markdown(f"##### {d['title']}")
            st.code(d["query"], language="text")
            st.markdown(f"[👉 Eksekusi Pencarian Langsung di Google]({d['link']})")
            st.write("")
            
        st.divider()
        st.subheader("📥 Export Official Audit Report")
        
        c_exp1, c_exp2, c_exp3 = st.columns(3)
        
        html_report = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>OSINT Audit Report - {res['name_in'] or res['email_in']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; padding: 30px; color: #0f172a; background-color: #ffffff; }}
                h1 {{ color: #1e293b; border-bottom: 3px solid #3b82f6; padding-bottom: 10px; }}
                .box {{ border: 1px solid #cbd5e1; padding: 18px; border-radius: 8px; margin-bottom: 20px; background-color: #f8fafc; }}
                .score {{ font-weight: bold; font-size: 22px; color: {'#16a34a' if res['risk_score']>=80 else '#dc2626'}; }}
                .footer {{ margin-top: 50px; font-size: 11px; text-align: center; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 12px; }}
            </style>
        </head>
        <body>
            <h1>🛡️ Official OSINT Executive Candidate Audit</h1>
            <div class="box">
                <p><b>Nama Kandidat:</b> {res['name_in'] or 'N/A'}</p>
                <p><b>Email Utama:</b> {mask_text(res['email_in'], 'email')}</p>
                <p><b>Nomor Kontak:</b> {mask_text(res['phone_data']['local_format'], 'phone')} ({res['phone_data']['provider']})</p>
                <p><b>Kota / Domisili:</b> {res['city_in'] or 'N/A'}</p>
                <p><b>Perusahaan / Instansi:</b> {res['company_in'] or 'N/A'}</p>
                <p><b>Timestamp Audit:</b> {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")} WIB</p>
                <p><b>Risk Score:</b> <span class="score">{res['risk_score']} / 100</span></p>
            </div>
            <div class="box">
                <h3>Temuan & Catatan Audit OSINT:</h3>
                <ul>
                    {''.join([f'<li>{n}</li>' for n in res['risk_notes']]) if res['risk_notes'] else '<li>Tidak ditemukan rekam jejak digital berisiko tinggi.</li>'}
                </ul>
            </div>
            <div class="footer">
                Generated by OSINT Enterprise Intelligence Platform v4.0 • Created by iqbalmantam
            </div>
        </body>
        </html>
        """
        
        c_exp1.download_button(
            label="📄 Export Printable (.HTML)",
            data=html_report,
            file_name=f"OSINT_Report_{res['email_in'].split('@')[0]}.html",
            mime="text/html",
            use_container_width=True
        )
        
        json_data = json.dumps(res, default=str, indent=2)
        c_exp2.download_button(
            label="📦 Export Full Raw (.JSON)",
            data=json_data,
            file_name=f"OSINT_Data_{res['email_in'].split('@')[0]}.json",
            mime="application/json",
            use_container_width=True
        )
        
        summary_df = pd.DataFrame([{
            "Nama": res["name_in"],
            "Email": res["email_in"],
            "Phone": res["phone_data"]["local_format"],
            "Provider": res["phone_data"]["provider"],
            "Risk Score": res["risk_score"],
            "Is Breached": res["is_breached"]
        }])
        c_exp3.download_button(
            label="📊 Export Summary (.CSV)",
            data=summary_df.to_csv(index=False),
            file_name=f"OSINT_Summary_{res['email_in'].split('@')[0]}.csv",
            mime="text/csv",
            use_container_width=True
        )
