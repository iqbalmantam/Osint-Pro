import streamlit as st
import asyncio
import pandas as pd

from modules.indo_telecom import analyze_indonesia_phone
from modules.identity_osint import check_email_identity
from modules.social_osint import check_indonesia_socials
from modules.breach_checker import check_data_breach
from modules.dork_indonesia import generate_indonesia_dorks

st.set_page_config(
    page_title="Indonesia Candidate OSINT Master",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: Menyembunyikan logo GitHub & posisi watermark di tengah bawah
st.markdown("""
    <style>
    /* Sembunyikan Header bawaan Streamlit (Logo GitHub, Share, Star) */
    header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0%;
    }
    
    /* Custom Watermark Melayang di Tengah Bawah */
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

st.title("🛡️ Indonesia Candidate OSINT Intelligence Engine")
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

    # Watermark Tambahan di bagian Bawah Sidebar
    st.markdown("<br><br><div style='text-align: center; color: #8b949e; font-size: 12px;'>Engine OSINT v2.0<br><b>Created by iqbalmantam</b></div>", unsafe_allow_html=True)

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

        # UI Tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "📱 Telecom & Primary Identity", 
            "🌐 Social Media Matrix", 
            "⚠️ Leak & Breach Intelligence",
            "⚖️ Legal & Court Dorking"
        ])

        # TAB 1: Telecom & Identity
        with tab1:
            st.subheader("📱 Analytics Seluler Indonesia")
            col_tel1, col_tel2, col_tel3 = st.columns(3)
            col_tel1.metric("Provider Seluler", phone_data["provider"])
            col_tel2.metric("Format Lokal", phone_data["local_format"])
            col_tel3.metric("Format Internasional", phone_data["intl_format"])
            
            st.markdown(f"* 🔗 [Buka Live Chat WhatsApp Kandidat]({phone_data['wa_link']})")
            st.markdown(f"* 🔗 [Cek Profil Telegram via Phone Number]({phone_data['telegram_link']})")
            
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
                active_count = len([s for s in social_res if s["found"]])
                st.metric("Total Platform Medsos Aktif", f"{active_count} / {len(social_res)}")
                
                df_s = pd.DataFrame(social_res)
                df_s["Status Network"] = df_s["found"].apply(lambda x: "✅ TERAKREDITASI AKTIF (200 OK)" if x else "❌ Tidak Ditemukan")
                st.dataframe(
                    df_s[["platform", "Status Network", "url"]], 
                    column_config={"url": st.column_config.LinkColumn("Direct Profile Link")},
                    use_container_width=True
                )
            else:
                st.info("Masukkan username di sidebar untuk memindai akun media sosial.")

        # TAB 3: Breach Intelligence
        with tab3:
            st.subheader("⚠️ Data Leakage Check")
            if breach_res.get("breached"):
                st.error("⚠️ WARN: Email ini ditemukan dalam insiden kebocoran data publik!")
                st.json(breach_res.get("data"))
            else:
                st.success("✅ Email ini bersih dan tidak terdeteksi dalam insiden kebocoran data publik besar.")

        # TAB 4: Legal & Court Dorking
        with tab4:
            st.subheader("⚖️ Legal & Court Precision Search")
            st.write("Dorking terisolasi untuk mendeteksi rekam jejak publik tanpa false positive:")
            
            for d in dorks:
                st.markdown(f"##### {d['title']}")
                st.code(d["query"], language="text")
                st.markdown(f"[👉 Eksekusi Pencarian Langsung di Google]({d['link']})")
                st.write("")
