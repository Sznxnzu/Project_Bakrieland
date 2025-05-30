import streamlit as st
import random
from streamlit_lottie import st_lottie
import requests

# --- Page Config ---
st.set_page_config(layout="wide", page_title="Bakrieland Project", initial_sidebar_state="collapsed")

# --- Lottie Loader ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_robot = load_lottieurl("lottie_robot = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_touohxv0.json")  # Robot mengetik

# --- Custom CSS ---
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/husnanali05/FP_Datmin/main/Halaman%20Utama%20Aplikasi.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: #E6E6E6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .header-with-bg {
        background-color: rgba(0,0,0,0.5);
        border: 2px solid #00f0ff;
        border-radius: 8px;
        padding: 4px;
        margin-bottom: 10px;
        text-align: center;
        color: #00f0ff;
        font-weight: bold;
    }
    .recommendation-box {
        border: 2px solid #00f0ff;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 0 15px rgba(0, 123, 255, 0.5);
        background-color: rgba(13, 18, 28, 0.85);
        text-align: center;
    }
    .recommendation-box img {
        border-radius: 5px;
        margin-bottom: 5px;
    }
    .mood-box {
        border: 2px solid #00f0ff;
        background-color: rgba(10, 15, 30, 0.8);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 0 20px #00f0ff;
        font-size: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Header ---
col_left, col_right = st.columns([0.85, 0.15])

with col_right:
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/bakrieland_logo.png", width=130)
    st.markdown("""
        <p style='text-align:right; font-size: 0.8em; color:#aaa;'>POWERED BY<br>
        <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/google_logo.png' width='60'>
        <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/metrodata_logo.png' width='40'>
        </p>
    """, unsafe_allow_html=True)

# --- Layout Section ---
col1, col2, col3 = st.columns([1, 1, 1.4])

with col1:
    st.markdown('<div class="header-with-bg">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="KAHURIPAN NIRWANA", use_container_width=True)
        st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="BOGOR NIRWANA RESIDENCE", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-with-bg">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="JUNGLE SEA", use_container_width=True)
        st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="RIVERA OUTBOND", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="header-with-bg">MOOD ANALYTIC</div>', unsafe_allow_html=True)
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

            <p><strong>Properti:</strong></p>
            <ul>
                <li>Apartemen Mewah di Pusat Kota: Fasilitas lengkap, pemandangan kota, dan privasi.</li>
                <li>Villa Eksklusif: Kolam renang pribadi dan suasana alam tenang.</li>
                <li>Rumah Klasik Modern: Arsitektur yang indah dan interior kristal.</li>
            </ul>

            <p><strong>Rekomendasi Liburan:</strong></p>
            <ul>
                <li>Resort Mewah: Pantai pribadi dan layanan premium tanpa gangguan.</li>
                <li>City Tour & Kuliner: Eksplorasi kota dan budaya lokal.</li>
                <li>Kapal Pesiar: Relaksasi, hiburan, dan pengalaman baru.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st_lottie(lottie_robot, height=200)
    else:
        st.markdown("<p style='color:#ccc;'>Silakan aktifkan kamera untuk memulai analisis mood.</p>", unsafe_allow_html=True)
        st_lottie(lottie_robot, height=200)
