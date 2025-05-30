import streamlit as st
import random

st.set_page_config(layout="wide", page_title="Bakrieland Project", initial_sidebar_state="collapsed")

# --- Custom CSS + dotlottie-player setup ---
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
        color: #00f0ff;
        font-size: 18px;
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
    .mood-box {
        border: 2px solid #00f0ff;
        background-color: rgba(10, 15, 30, 0.85);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 0 20px #00f0ff;
        font-size: 15px;
        margin-bottom: 20px;
    }
    </style>

    <script src="https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs" type="module"></script>
""", unsafe_allow_html=True)

# --- Header Branding ---
col_left, col_right = st.columns([0.85, 0.15])
with col_right:
    st.image("https://raw.githubusercontent.com/Sznxnzu/import streamlit as st
import random

st.set_page_config(layout="wide", page_title="Bakrieland Project", initial_sidebar_state="collapsed")

# --- Custom CSS + iframe-safe animation ---
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
        color: #00f0ff;
        font-size: 18px;
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
    .mood-box {
        border: 2px solid #00f0ff;
        background-color: rgba(10, 15, 30, 0.85);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 0 20px #00f0ff;
        font-size: 15px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
col_left, col_right = st.columns([0.85, 0.15])
with col_right:
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/bakrieland_logo.png", width=130)
    st.markdown("""
        <p style='text-align:right; font-size: 0.8em; color:#aaa;'>POWERED BY<br>
        <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/google_logo.png' width='60'>
        <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/metrodata_logo.png' width='40'>
        </p>
    """, unsafe_allow_html=True)

# --- 3-Column Layout ---
col1, col2, col3 = st.columns([1, 1, 1.4])

with col1:
    st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="KAHURIPAN NIRWANA", use_container_width=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="BOGOR NIRWANA RESIDENCE", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="JUNGLE SEA", use_container_width=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="RIVERA OUTBOND", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="header-box">MOOD ANALYTIC</div>', unsafe_allow_html=True)
    picture = st.camera_input("")

    if picture:
        st.image(picture, width=150)

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

    # ROBOT Animation via iframe
    st.markdown("""
    <div style="text-align: center;">
        <iframe src="https://lottie.host/?file=361e18c3-a1dc-4e6b-af1e-6dcdded54c47/yY2N31uIA2.lottie"
                width="300" height="300" style="border: none;" allowfullscreen></iframe>
    </div>
    """, unsafe_allow_html=True)
oject_Bakrieland/main/bakrieland_logo.png", width=130)
    st.markdown("""
        <p style='text-align:right; font-size: 0.8em; color:#aaa;'>POWERED BY<br>
        <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/google_logo.png' width='60'>
        <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/metrodata_logo.png' width='40'>
        </p>
    """, unsafe_allow_html=True)

# --- Content Area ---
col1, col2, col3 = st.columns([1, 1, 1.4])

with col1:
    st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="KAHURIPAN NIRWANA", use_container_width=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="BOGOR NIRWANA RESIDENCE", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="JUNGLE SEA", use_container_width=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="RIVERA OUTBOND", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="header-box">MOOD ANALYTIC</div>', unsafe_allow_html=True)
    picture = st.camera_input("")

    if picture:
        st.image(picture, width=150)

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

    # --- DotLottie Robot Animation (ALWAYS SHOW) ---
    st.markdown("""
        <div style="text-align: center;">
            <dotlottie-player
                src="https://lottie.host/361e18c3-a1dc-4e6b-af1e-6dcdded54c47/yY2N31uIA2.lottie"
                background="transparent"
                speed="1"
                style="width: 280px; height: 280px;"
                loop
                autoplay
            ></dotlottie-player>
        </div>
    """, unsafe_allow_html=True)
