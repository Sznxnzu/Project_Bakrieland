import streamlit as st
import random

st.set_page_config(layout="wide", page_title="Bakrieland Project", initial_sidebar_state="collapsed")

# --- CSS Styling ---
st.markdown("""
<style>
.stApp {
    background-image: url("https://raw.githubusercontent.com/husnanali05/FP_Datmin/main/Halaman%20Utama%20Aplikasi.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

.header-box {
    text-align: center;
    border: 2px solid #00f0ff;
    background-color: rgba(0,0,50,0.5);
    border-radius: 8px;
    padding: 6px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px #00f0ff;
}

.header-box h3 {
    margin: 0;
    font-size: 18px;
    color: #00f0ff;
}

.content-box {
    border: 2px solid #00f0ff;
    background-color: rgba(0,0,30,0.6);
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
    text-align: center;
    box-shadow: 0 0 10px #00f0ff;
}

.content-box img {
    border: 3px solid #00f0ff;
    border-radius: 4px;
    margin-bottom: 8px;
}

.mood-box {
    border: 2px solid #00f0ff;
    background-color: rgba(10, 15, 30, 0.8);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 20px #00f0ff;
    font-size: 15px;
}

.mood-box ul {
    padding-left: 20px;
}

.qr-and-robot {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
col_left, col_right = st.columns([0.85, 0.15])

with col_right:
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/bakrieland_logo.png", width=130)
    st.markdown("""
        <p style='text-align:right; font-size: 0.8em; color:#aaa;'>POWERED BY<br>
        <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/google_logo.png' width='60'>
        <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/metrodata_logo.png' width='40'>
        </p>
    """, unsafe_allow_html=True)

# --- MAIN SECTION ---
col1, col2, col3 = st.columns([1, 1, 1.4])

# PROPERTY RECOMMENDATION
with col1:
    st.markdown('<div class="header-box"><h3>PROPERTY RECOMMENDATION</h3></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="KAHURIPAN NIRWANA", use_container_width=True)
        st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="BOGOR NIRWANA RESIDENCE", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# HOLIDAY RECOMMENDATION
with col2:
    st.markdown('<div class="header-box"><h3>HOLIDAY RECOMMENDATION</h3></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="JUNGLE SEA", use_container_width=True)
        st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="RIVERA OUTBOND", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# MOOD ANALYTIC SECTION
with col3:
    st.markdown('<div class="header-box"><h3>MOOD ANALYTIC</h3></div>', unsafe_allow_html=True)
    picture = st.camera_input("")

    if picture:
        mood = "Percaya Diri"
        st.image(picture, width=150)

        st.markdown(f"""
        <div class="mood-box">
            <p><strong>Analisa Mood:</strong></p>
            <ul>
                <li>Percaya Diri: Terlihat dari sorot matanya dan posisi wajahnya.</li>
                <li>Elegan/Glamor: Penampilannya secara keseluruhan memberikan kesan ini.</li>
                <li>Tenang/Terkontrol: Tidak ada tanda-tanda kegelisahan atau kekacauan.</li>
            </ul>
            <p><strong>Property:</strong></p>
            <ul>
                <li>Apartemen Mewah di Pusat Kota: Dengan fasilitas lengkap seperti gym dan pemandangan kota.</li>
                <li>Hunian Bergaya Klasik Modern: Desain elegan berpadu interior kristal dan marmer.</li>
                <li>Villa Eksklusif: Dikelilingi alam terbuka dengan kolam renang pribadi.</li>
            </ul>
            <p><strong>Rekomendasi Liburan yang Cocok:</strong></p>
            <ul>
                <li>Liburan Santai di Resort Mewah: Pantai pribadi, spa, dan layanan premium.</li>
                <li>Perjalanan Belanja & Kuliner di Kota Bogor.</li>
                <li>Pelayaran Kapal Pesiar Mewah: Hiburan, relaksasi dan pengalaman baru.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="qr-and-robot">
            <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" width="120">
            <img src="https://api.qrserver.com/v1/create-qr-code/?size=100x100&data=https://bakrieland.com" width="80">
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='color:#ccc;'>Silakan aktifkan kamera untuk analisis mood otomatis.</p>", unsafe_allow_html=True)
