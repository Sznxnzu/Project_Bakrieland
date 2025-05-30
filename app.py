
import streamlit as st

st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# --- CSS ---
st.markdown("""
<style>
.stApp {
    background-image: url("https://raw.githubusercontent.com/husnanali05/FP_Datmin/main/Halaman%20Utama%20Aplikasi.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    font-family: 'Segoe UI', sans-serif;
    color: white;
}
.header-box {
    text-align: center;
    border: 2px solid #00f0ff;
    background-color: rgba(0,0,50,0.5);
    border-radius: 8px;
    padding: 6px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px #00f0ff;
    color: #00f0ff;
    font-size: 18px;
}
.portrait-box {
    border: 2px solid #00f0ff;
    background-color: rgba(0,0,30,0.6);
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px #00f0ff;
    text-align: center;
}
.mood-box {
    border: 2px solid #00f0ff;
    background-color: rgba(10, 15, 30, 0.85);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 20px #00f0ff;
    font-size: 15px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

# --- dotlottie script for transparent robot animation ---
st.markdown("""
<script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>
""", unsafe_allow_html=True)

# --- HEADER ---
col_header_left, col_header_right = st.columns([0.8, 0.2])
with col_header_right:
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/bakrieland_logo.png", width=120)
    st.markdown("""
    <p style='text-align:right; font-size: 0.8em; color:#aaa;'>POWERED BY<br>
    <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/google_logo.png' width='50'>
    <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/metrodata_logo.png' width='35'>
    </p>
    """, unsafe_allow_html=True)

# --- MAIN 3-COLUMN LAYOUT ---
col1, col2, col3 = st.columns([1, 1, 1.4])

with col1:
    st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="portrait-box">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="KAHURIPAN NIRWANA", use_column_width=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="BOGOR NIRWANA RESIDENCE", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="portrait-box">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="JUNGLE SEA", use_column_width=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="RIVERA OUTBOND", use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="header-box">MOOD ANALYTIC</div>', unsafe_allow_html=True)
    picture = st.camera_input("")

    if picture:
        st.image(picture, width=200)
        st.markdown("""
        <div class="mood-box">
            <p><strong>Analisa Mood:</strong></p>
            <ul>
                <li>Percaya Diri: Terlihat dari sorot matanya dan posisi wajahnya.</li>
                <li>Elegan/Glamor: Penampilannya secara keseluruhan memberikan kesan ini.</li>
                <li>Tenang/Terkontrol: Tidak ada tanda-tanda kegelisahan atau kekacauan.</li>
            </ul>
            <p><strong>Property:</strong></p>
            <ul>
                <li>Apartemen Mewah di Pusat Kota</li>
                <li>Hunian Klasik Modern</li>
                <li>Villa Eksklusif Pemandangan Alam</li>
            </ul>
            <p><strong>Rekomendasi Liburan:</strong></p>
            <ul>
                <li>Liburan Santai di Resort</li>
                <li>Perjalanan Kuliner Kota</li>
                <li>Kapal Pesiar Mewah</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # --- Transparent Lottie Robot ---
    st.markdown("""
    <div style="text-align: center;">
        <dotlottie-player
            src="https://lottie.host/361e18c3-a1dc-4e6b-af1e-6dcdded54c47/yY2N31uIA2.lottie"
            background="transparent"
            speed="1"
            style="width: 300px; height: 300px;"
            loop
            autoplay>
        </dotlottie-player>
    </div>
    """, unsafe_allow_html=True)
