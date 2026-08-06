import streamlit as st
import asyncio
import pandas as pd
import json
from urllib.parse import quote_plus

from modules.indo_telecom import analyze_indonesia_phone
from modules.identity_osint import check_email_identity
from modules.social_osint import check_indonesia_socials
from modules.breach_checker import check_data_breach
from modules.dork_indonesia import generate_indonesia_dorks, generate_telecom_dorks

st.set_page_config(
    page_title="Background Check",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: Menyembunyikan header bawaan Streamlit & Watermark di tengah bawah
st.markdown("""
    <style>
    header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0%;
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

    st.markdown("<br><br><div style='text-align: center; color: #8b949e; font-size: 12px;'>Engine OSINT v2.5<br><b>Created by iqbalmantam</b></div>", unsafe_allow_html=True)

if btn_submit:
    if not email_in or not phone_in:
        st.error("⚠️ Email dan Nomor HP Wajib Diisi sebagai Primary Anchor Key!")
    else:
        phone_data = analyze_indonesia_phone(phone_in)
        st.toast("Menghubungkan ke server jaringan publik secara real-time...", icon="🔄")
        
        # Async Executions
        identity_res = asyncio.run(check_email_identity(email_in))
        social_res = asyncio.run(check_indonesia_socials(username_in)) if username_in else []
        breach_res = asyncio.run(check_data_breach(email_in))
        dorks = generate_indonesia_dorks(email_in, phone_data, username_in, name_in)
        telecom_links = generate_telecom_dorks(phone_data["intl_format"])

        # ==========================================
        # FITUR 4: RISK SCORING ENGINE
        # ==========================================
        active_social_count = len([s for s in social_res if s["found"]]) if social_res else 0
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
        if active_social_count == 0 and username_in:
            risk_score -= 20
            risk_notes.append("Username yang dimasukkan tidak terdeteksi aktif di platform medsos utama.")

        # Risk Banner
        st.subheader("📊 Summary & Digital Footprint Risk Score")
        col_risk1, col_risk2 = st.columns([1, 2])
        
        with col_risk1:
            if risk_score >= 80:
                st.success(f"### Score: {risk_score}/100 (LOW RISK)")
            elif risk_score >= 50:
                st.warning(f"### Score: {risk_score}/100 (MEDIUM RISK)")
            else:
                st.error(f"### Score: {risk_score}/100 (HIGH RISK)")
                
        with col_risk2:
            st.write("**Catatan Evaluasi Otomatis:**")
            if risk_notes:
                for note in risk_notes:
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

        # TAB 1: Telecom & Identity + GetContact/Truecaller
        with tab1:
            st.subheader("📱 Analytics Seluler & Tags Lookup")
            col_tel1, col_tel2, col_tel3 = st.columns(3)
            col_tel1.metric("Provider Seluler", phone_data["provider"])
            col_tel2.metric("Format Lokal", phone_data["local_format"])
            col_tel3.metric("Format Internasional", phone_data["intl_format"])
            
            st.markdown(f"* 💬 [Buka Live Chat WhatsApp Kandidat]({phone_data['wa_link']})")
            st.markdown(f"* ✈️ [Cek Profil Telegram via Phone Number]({phone_data['telegram_link']})")
            st.markdown(f"* 📞 [Pindai Tags/Nama Kontak via Truecaller]({telecom_links['truecaller']})")
            st.markdown(f"* 📇 [Akses GetContact Unbind/Lookup Page]({telecom_links['getcontact']})")
            
            st.divider()
            
            st.subheader("👤 Identitas Utama Terikat Email")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Gravatar / WordPress Global")
                g = identity_res.get("gravatar", {})
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
                gh = identity_res.get("github", {})
                if gh.get("found"):
                    st.success("AKUN AKTIF TERDAFTAR")
                    if gh.get("avatar"): st.image(gh["avatar"], width=80)
                    st.write(f"**Username:** @{gh.get('username')}")
                    st.write(f"**Public Repos:** {gh.get('repos')}")
                    st.write(f"**Bio / Perusahaan:** {gh.get('bio')} | {gh.get('company')}")
                    st.markdown(f"[🔗 Buka Repositori GitHub]({gh.get('profile_url')})")
                else:
                    st.info("Email tidak terikat GitHub publik.")

        # TAB 2: Social Matrix
        with tab2:
            st.subheader("🌐 Matrix Media Sosial Active Check")
            if social_res:
                st.metric("Total Platform Medsos Aktif", f"{active_social_count} / {len(social_res)}")
                df_s = pd.DataFrame(social_res)
                df_s["Status Network"] = df_s["found"].apply(lambda x: "✅ TERAKREDITASI AKTIF (200 OK)" if x else "❌ Tidak Ditemukan")
                st.dataframe(
                    df_s[["platform", "Status Network", "url"]], 
                    column_config={"url": st.column_config.LinkColumn("Direct Profile Link")},
                    use_container_width=True
                )
            else:
                st.info("Masukkan username di sidebar untuk memindai akun media sosial.")

        # TAB 3: REVERSE IMAGE SEARCH ENGINE
        with tab3:
            st.subheader("🖼️ Reverse Image Search Engine")
            st.write("Analisis foto kandidat ke berbagai mesin pencari visual untuk mendeteksi keaslian profil:")
            
            avatar_url = identity_res.get("gravatar", {}).get("avatar") or identity_res.get("github", {}).get("avatar")
            
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
            if breach_res.get("breached"):
                st.error("⚠️ WARN: Email ini ditemukan dalam insiden kebocoran data publik!")
                st.json(breach_res.get("data"))
            else:
                st.success("✅ Email ini bersih dan tidak terdeteksi dalam insiden kebocoran data publik besar.")

        # TAB 5: Legal Dorking & Report Download
        with tab5:
            st.subheader("⚖️ Legal & Court Precision Search")
            for d in dorks:
                st.markdown(f"##### {d['title']}")
                st.code(d["query"], language="text")
                st.markdown(f"[👉 Eksekusi Pencarian Langsung di Google]({d['link']})")
                st.write("")
                
            st.divider()
            
            # FITUR EXPORT REPORT (JSON)
            st.subheader("📥 Export Audit Report")
            report_data = {
                "candidate_name": name_in or "N/A",
                "email": email_in,
                "phone": phone_data["local_format"],
                "provider": phone_data["provider"],
                "risk_score": risk_score,
                "active_social_platforms": [s["platform"] for s in social_res if s.get("found")],
                "breached": is_breached,
                "audit_timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            report_json = json.dumps(report_data, indent=4)
            st.download_button(
                label="📥 Download Audit Report (.JSON)",
                data=report_json,
                file_name=f"OSINT_Report_{email_in.split('@')[0]}.json",
                mime="application/json"
            )
