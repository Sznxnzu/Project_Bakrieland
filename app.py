import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import random

# --- Konfigurasi Halaman ---
st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# --- CSS LENGKAP DENGAN STRUKTUR TUNGGAL ---
st.markdown("""
<style>
/* --- Reset & Gaya Dasar --- */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: #19307f !important;
}
::-webkit-scrollbar { display: none; }
.block-container {
    padding: 1rem !important;
}

/* --- KELAS UTAMA UNTUK KONTROL LAYOUT --- */
.main-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
}

/* --- TATA LETAK MOBILE (DEFAULT, max-width: 768px) ---
Ini adalah tampilan dasar, semua elemen akan mengikuti gaya ini 
kecuali diubah oleh media query untuk desktop.
*/

/* (Mobile) Sembunyikan sidebar desktop */
.desktop-sidebar {
    display: none;
}

/* (Mobile) Header dengan semua logo */
.mobile-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 95%;
    margin-bottom: 20px;
}
.mobile-header .left-logos { display: flex; align-items: center; }
.mobile-header .left-logos img { height: 35px; margin-right: 8px; }
.mobile-header .right-logo img { height: 40px; }

/* (Mobile & Desktop) Wrapper Kamera */
.camera-wrapper {
    position: relative;
    margin-bottom: 60px; /* Memberi ruang untuk tombol di bawahnya */
}

/* (Mobile) Ukuran Kamera */
.camera-wrapper div[data-testid="stCameraInput"],
.camera-wrapper div[data-testid="stCameraInputWebcamStyledBox"],
.camera-wrapper div[data-testid="stCameraInput"] video,
.camera-wrapper div[data-testid="stCameraInput"] img {
    width: 220px !important;
    height: 220px !important;
    border-radius: 50% !important;
    object-fit: cover;
    margin: 0 auto;
}
.camera-wrapper div[data-testid="stCameraInput"] button {
    width: 120px;
    font-size: 14px;
    position: absolute;
    bottom: -45px; /* Posisi di bawah bingkai kamera */
    left: 50%;
    transform: translateX(-50%);
}

/* (Mobile) Powered By Logos */
.mobile-poweredby {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 20px;
}
.mobile-poweredby .powered-by-text { font-size: 12px; color: #ccc; }
.mobile-poweredby .powered-by-logos { display: flex; align-items: center; }
.mobile-poweredby .powered-by-logos img { height: 25px !important; margin: 0 5px; }

/* (Shared) Mood Analytic & Recommendation Boxes */
.content-box {
    width: 95%;
    max-width: 600px; /* Batas lebar di desktop */
    margin-left: auto;
    margin-right: auto;
}
.header-box, .portrait-box {
    border: 2px solid #00f0ff;
    background-color: rgba(0,0,50,0.5);
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px #00f0ff;
    color: #00f0ff;
}
.header-box { font-size: 18px; text-align: center; }
.portrait-box { background-color: rgba(0,0,30,0.6); text-align: center; }
.portrait-box img { max-height: 180px; width: 100%; object-fit: cover; border-radius: 8px; }
.portrait-box p { font-size: 18px; color: #ccc; margin-top: 5px; }
.mood-box-content h2 { font-size: 22px; text-align: center; margin:0; padding:0; }
.mood-box-content pre { font-size: 14px; text-align: center; white-space: pre-wrap; font-family: inherit; }


/* --- TATA LETAK DESKTOP (min-width: 769px) ---
Mengatur ulang elemen yang SUDAH ADA untuk tampilan layar lebar.
*/
@media (min-width: 769px) {
    .block-container {
        padding-top: 2rem !important;
    }
    
    /* Buat layout grid 3 kolom */
    .main-container {
        display: grid;
        grid-template-columns: 0.2fr 0.6fr 0.2fr; /* Rasio kolom */
        grid-template-areas: "sidebar-left main-content sidebar-right";
        align-items: start;
        gap: 20px;
        width: 100%;
    }

    /* Sembunyikan header dan powered-by versi mobile */
    .mobile-header, .mobile-poweredby {
        display: none;
    }
    
    /* Tampilkan sidebar desktop dan atur isinya */
    .desktop-sidebar {
        display: flex;
        flex-direction: column;
        align-items: center;
        height: 500px;
    }
    .desktop-sidebar#left { grid-area: sidebar-left; justify-content: space-between; }
    .desktop-sidebar#right { grid-area: sidebar-right; justify-content: center; text-align: center;}
    
    .desktop-sidebar .logo-box img { width: 150px; }
    .desktop-sidebar#right .logo-box img { height: 70px; width: auto; margin-bottom: 20px;}
    .desktop-sidebar .powered-by-text { color: white; }
    .desktop-sidebar .powered-by-logos img { height: 40px; }
    
    /* Atur area konten utama di tengah */
    .main-content-area {
        grid-area: main-content;
        width: 100%;
    }

    /* (Desktop) Ukuran Kamera */
    .camera-wrapper { margin-bottom: 20px; }
    .camera-wrapper div[data-testid="stCameraInput"],
    .camera-wrapper div[data-testid="stCameraInputWebcamStyledBox"],
    .camera-wrapper div[data-testid="stCameraInput"] video,
    .camera-wrapper div[data-testid="stCameraInput"] img {
        width: 450px !important;
        height: 450px !important;
    }
    .camera-wrapper div[data-testid="stCameraInput"] button {
        bottom: 20px; right: 20px; transform: none; left: auto;
    }
    
    /* Atur agar rekomendasi berdampingan di desktop */
    .recommendations-wrapper {
        display: flex;
        gap: 15px;
        width: 100%;
        max-width: none; /* Hapus max-width mobile */
    }
    .recommendation-col { flex: 1; }
}
</style>
""", unsafe_allow_html=True)


# --- State Management ---
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati."
    st.session_state.image_urls = ["https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"] * 4
    st.session_state.image_captions = [""] * 4
    st.session_state.last_photo = None
    
# --- Konfigurasi API ---
try:
    genai.configure(api_key=st.secrets["gemini_api"])
    MODEL = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Gagal mengkonfigurasi API: {e}")
    st.stop()


# --- Image Processing Logic ---
def process_image(user_input_bytes):
    # (Fungsi ini tidak perlu diubah)
    with st.spinner("Menganalisis suasana hati Anda..."):
        try:
            image = Image.open(io.BytesIO(user_input_bytes.getvalue()))
            prompt_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt.txt"
            analysis_prompt = requests.get(prompt_url).text
            json_prompt_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt_json.txt"
            json_prompt = requests.get(json_prompt_url).text

            analysis_response = MODEL.generate_content([analysis_prompt, image])
            raw_output = analysis_response.text
            json_response = MODEL.generate_content([json_prompt, raw_output])
            filenames = [name.strip() for name in json_response.text.strip().split(",")]

            if len(filenames) >= 4:
                st.session_state.analysis_result = raw_output
                st.session_state.image_urls = [
                    f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{filenames[0]}.jpg",
                    f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{filenames[1]}.jpg",
                    f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{filenames[2]}.jpg",
                    f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{filenames[3]}.jpg"
                ]
                st.session_state.image_captions = filenames
            else:
                st.session_state.analysis_result = "Gagal memproses rekomendasi. Silakan coba lagi."
        except Exception as e:
            st.error(f"Terjadi kesalahan saat pemrosesan: {e}")
            st.session_state.analysis_result = "Gagal menganalisis gambar. Silakan coba lagi."


# --- STRUKTUR HTML TUNGGAL ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# --- Sidebar Kiri (Hanya Tampil di Desktop) ---
st.markdown("""
<div class="desktop-sidebar" id="left">
    <div class="logo-box"><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/35thn_logo.png"></div>
    <div class="logo-box"><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/mascot_logo.png"></div>
</div>
""", unsafe_allow_html=True)

# --- Konten Utama (Tampil di Mobile & Desktop) ---
st.markdown('<div class="main-content-area">', unsafe_allow_html=True)

# Header (Hanya Tampil di Mobile)
st.markdown("""
<header class="mobile-header">
    <div class="left-logos">
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/35thn_logo.png">
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/mascot_logo.png">
    </div>
    <div class="right-logo">
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png">
    </div>
</header>
""", unsafe_allow_html=True)

# Kamera
with st.container():
    st.markdown('<div class="camera-wrapper">', unsafe_allow_html=True)
    user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")
    st.markdown('</div>', unsafe_allow_html=True)

# Powered By (Hanya Tampil di Mobile)
st.markdown("""
<div class="mobile-poweredby">
    <div class="powered-by-text">POWERED BY:</div>
    <div class="powered-by-logos">
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png">
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png">
    </div>
</div>
""", unsafe_allow_html=True)

# Mood Analytic Box
with st.container():
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    escaped_analysis = html.escape(st.session_state.analysis_result)
    st.markdown(f"""
    <div class="header-box mood-box-content">
      <h2>Mood Analytic</h2>
      <pre>{escaped_analysis}</pre>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Recommendations
with st.container():
    st.markdown('<div class="recommendations-wrapper">', unsafe_allow_html=True)
    
    st.markdown('<div class="recommendation-col">', unsafe_allow_html=True)
    st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="portrait-box">
        <img src="{st.session_state.image_urls[0]}">
        <p>{st.session_state.image_captions[0]}</p>
        <img src="{st.session_state.image_urls[1]}">
        <p>{st.session_state.image_captions[1]}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="recommendation-col">', unsafe_allow_html=True)
    st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="portrait-box">
        <img src="{st.session_state.image_urls[2]}">
        <p>{st.session_state.image_captions[2]}</p>
        <img src="{st.session_state.image_urls[3]}">
        <p>{st.session_state.image_captions[3]}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Penutup .main-content-area

# --- Sidebar Kanan (Hanya Tampil di Desktop) ---
st.markdown("""
<div class="desktop-sidebar" id="right">
    <div class="logo-box"><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png"></div>
    <div class="powered-by-text">POWERED BY:</div>
    <div class="powered-by-logos">
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png">
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png">
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Penutup .main-container


# --- Logika Pemicu Pemrosesan Gambar ---
if user_input and user_input != st.session_state.get('last_photo'):
    st.session_state.last_photo = user_input
    process_image(user_input)
    st.rerun()

elif not user_input and st.session_state.get('last_photo'):
    st.session_state.last_photo = None
    # Reset ke placeholder jika kamera ditutup
    st.session_state.analysis_result = "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati."
    st.session_state.image_urls = ["https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"] * 4
    st.session_state.image_captions = [""] * 4
    st.rerun()


# --- Tombol Screenshot ---
components.html("""
<html><body>
    <button id="screenshotBtn" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; background-color: #00c0cc; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 12px rgba(0, 240, 255, 0.6);">📸 QRCODE</button>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script>
      document.getElementById("screenshotBtn").addEventListener("click", function () {
        const mainContent = parent.document.querySelector('.main-container');
        html2canvas(mainContent).then(canvas => {
          const link = document.createElement("a");
          link.download = "mood-analytic-bakrieland.png";
          link.href = canvas.toDataURL();
          link.click();
        });
      });
    </script>
</body></html>
""", height=50)