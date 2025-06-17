import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import random

# Konfigurasi Halaman
st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# --- CSS BARU UNTUK TATA LETAK FINAL ---
st.markdown("""
<style>
/* --- Reset & Gaya Dasar --- */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: #19307f !important;
}
::-webkit-scrollbar { display: none; }
.block-container {
    padding: 1rem !important;
    max-width: 1200px !important;
}

/* --- KELAS-KELAS BARU UNTUK KONTROL LAYOUT --- */
.main-container {
    width: 100%;
}
.header-box, .portrait-box {
    border: 2px solid #00f0ff;
    background-color: rgba(0,0,50,0.5);
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px #00f0ff;
    color: #00f0ff;
    text-align: center;
}
.portrait-box { background-color: rgba(0,0,30,0.6); }

/* --- TATA LETAK MOBILE (DEFAULT, max-width: 768px) --- */

.main-container {
    display: grid;
    grid-template-columns: 1fr auto; /* Kolom utama fleksibel, kolom kanan auto */
    grid-template-rows: auto;
    gap: 10px 5px;
    grid-template-areas:
        "top-logo top-logo"
        "camera camera"
        "mascot right-stack"
        "analysis analysis"
        "recommendations recommendations";
}

.top-logo-wrapper   { grid-area: top-logo; }
.camera-wrapper     { grid-area: camera; justify-self: center; }
.mascot-wrapper     { grid-area: mascot; justify-self: center; align-self: start; }
.right-stack-wrapper{ grid-area: right-stack; justify-self: end; align-self: start;}
.analysis-wrapper   { grid-area: analysis; }
.recommendations-wrapper { grid-area: recommendations; }

.top-logo-wrapper img {
    width: 120px; /* Ukuran sedang untuk logo 35 tahun */
    height: auto;
}

.camera-wrapper div[data-testid="stCameraInput"],
.camera-wrapper div[data-testid="stCameraInputWebcamStyledBox"],
.camera-wrapper div[data-testid="stCameraInput"] video,
.camera-wrapper div[data-testid="stCameraInput"] img {
    width: 250px !important;
    height: 250px !important;
    border-radius: 50% !important;
    object-fit: cover;
    margin: 0 auto;
}
.camera-wrapper div[data-testid="stCameraInput"] button {
    width: 120px; font-size: 14px;
    position: absolute; bottom: 5px;
    left: 50%; transform: translateX(-50%);
}

.mascot-wrapper img {
    width: 80px;
    height: auto;
}

.right-stack-wrapper {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 8px;
}
.right-stack-wrapper .bakrieland-logo img {
    height: 40px;
    width: auto;
}
.right-stack-wrapper .powered-by-text {
    font-size: 11px;
    color: #ccc;
    text-align: right;
}
.right-stack-wrapper .powered-by-logos {
    display: flex;
    gap: 5px;
}
.right-stack-wrapper .powered-by-logos img {
    height: 20px;
}

.analysis-wrapper .header-box h2 { font-size: 22px; margin: 0; padding: 0; }
.analysis-wrapper .header-box pre { font-size: 14px; white-space: pre-wrap; font-family: inherit; }
.recommendations-wrapper { display: flex; flex-direction: column; }
.recommendations-wrapper .header-box { font-size: 18px; }

/* Sembunyikan sidebar desktop di mobile */
.desktop-sidebar { display: none; }


/* --- TATA LETAK DESKTOP (min-width: 769px) --- */
@media (min-width: 769px) {
    /* Atur ulang grid untuk 3 kolom desktop */
    .main-container {
        display: grid;
        grid-template-columns: 0.2fr 0.6fr 0.2fr;
        grid-template-rows: auto auto 1fr;
        gap: 20px;
        grid-template-areas:
            "sidebar-left camera sidebar-right"
            "sidebar-left analysis sidebar-right"
            "sidebar-left recommendations sidebar-right";
    }

    /* Sembunyikan elemen mobile yang tidak perlu */
    .top-logo-wrapper, .mascot-wrapper, .right-stack-wrapper {
        display: none;
    }

    /* Tampilkan dan posisikan sidebar desktop */
    .desktop-sidebar {
        display: flex;
        flex-direction: column;
        height: 100%;
    }
    .desktop-sidebar#left {
        grid-area: sidebar-left;
        justify-content: space-between;
        align-items: center;
    }
    .desktop-sidebar#right {
        grid-area: sidebar-right;
        justify-content: center;
        align-items: center;
        text-align: center;
        gap: 20px;
    }
    .desktop-sidebar .logo-box img { width: 150px; }
    .desktop-sidebar .powered-by-text { color: white; }
    .desktop-sidebar .powered-by-logos img { height: 40px; }
    
    /* Posisikan elemen utama di tengah */
    .camera-wrapper { grid-area: camera; }
    .analysis-wrapper { grid-area: analysis; }
    .recommendations-wrapper { grid-area: recommendations; }
    
    /* Atur kamera untuk desktop */
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
    
    /* Atur rekomendasi menjadi 2 kolom di desktop */
    .recommendations-wrapper {
        flex-direction: row;
        gap: 15px;
    }
    .recommendation-col { flex: 1; }
}
</style>
""", unsafe_allow_html=True)


# --- State Management & API Config ---
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = "Arahkan kamera ke wajah Anda untuk memulai analisis suasana hati."
    st.session_state.image_urls = ["https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"] * 4
    st.session_state.image_captions = [""] * 4
    st.session_state.last_photo = None

try:
    genai.configure(api_key=st.secrets["gemini_api"])
    MODEL = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Gagal mengkonfigurasi API: {e}")
    st.stop()


# --- Image Processing Logic ---
def process_image(user_input_bytes):
    # (Fungsi ini tidak diubah)
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
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")


# --- STRUKTUR HTML BARU YANG BERSIH ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Elemen untuk Sidebar Kiri (Hanya Tampil di Desktop)
st.markdown("""
<div class="desktop-sidebar" id="left">
    <div class="logo-box"><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/35thn_logo.png"></div>
    <div class="logo-box"><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/mascot_logo.png"></div>
</div>""", unsafe_allow_html=True)

# Elemen untuk Mobile: Logo 35 Tahun
st.markdown("""
<div class="top-logo-wrapper">
    <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/35thn_logo.png">
</div>""", unsafe_allow_html=True)

# Elemen untuk Mobile: Maskot Rusa
st.markdown("""
<div class="mascot-wrapper">
    <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/mascot_logo.png">
</div>""", unsafe_allow_html=True)

# Elemen untuk Mobile: Grup Logo Kanan
st.markdown("""
<div class="right-stack-wrapper">
    <div class="bakrieland-logo">
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png">
    </div>
    <div class="powered-by-text">POWERED BY:</div>
    <div class="powered-by-logos">
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png">
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png">
    </div>
</div>""", unsafe_allow_html=True)

# Elemen untuk Sidebar Kanan (Hanya Tampil di Desktop)
st.markdown("""
<div class="desktop-sidebar" id="right">
    <div class="logo-box"><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png"></div>
    <div>
        <div class="powered-by-text">POWERED BY:</div>
        <div class="powered-by-logos">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png">
        </div>
    </div>
</div>""", unsafe_allow_html=True)

# Elemen Kamera (Tampil di kedua layout)
with st.container():
    st.markdown('<div class="camera-wrapper">', unsafe_allow_html=True)
    user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")
    st.markdown('</div>', unsafe_allow_html=True)

# Elemen Analisis (Tampil di kedua layout)
with st.container():
    st.markdown('<div class="analysis-wrapper">', unsafe_allow_html=True)
    escaped_analysis = html.escape(st.session_state.analysis_result)
    st.markdown(f"""
    <div class="header-box mood-box-content">
      <h2>Mood Analytic</h2>
      <pre>{escaped_analysis}</pre>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Elemen Rekomendasi (Tampil di kedua layout)
with st.container():
    st.markdown('<div class="recommendations-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="recommendation-col">', unsafe_allow_html=True)
    st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="portrait-box">
        <img src="{st.session_state.image_urls[0]}"><p>{st.session_state.image_captions[0]}</p>
        <img src="{st.session_state.image_urls[1]}"><p>{st.session_state.image_captions[1]}</p>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="recommendation-col">', unsafe_allow_html=True)
    st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="portrait-box">
        <img src="{st.session_state.image_urls[2]}"><p>{st.session_state.image_captions[2]}</p>
        <img src="{st.session_state.image_urls[3]}"><p>{st.session_state.image_captions[3]}</p>
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True) # Penutup .main-container

# --- Logika Pemicu Pemrosesan Gambar ---
if user_input and user_input != st.session_state.get('last_photo'):
    st.session_state.last_photo = user_input
    process_image(user_input)
    st.rerun()
elif not user_input and st.session_state.get('last_photo'):
    st.session_state.last_photo = None
    st.rerun()

# --- Tombol Screenshot ---
components.html("""
<button id="screenshotBtn" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; background-color: #00c0cc; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 12px rgba(0, 240, 255, 0.6);">📸 Screenshot</button>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script>
  document.getElementById("screenshotBtn").addEventListener("click", function () {
    html2canvas(parent.document.querySelector('.main-container')).then(canvas => {
      const link = document.createElement("a");
      link.download = "mood-analytic-bakrieland.png";
      link.href = canvas.toDataURL();
      link.click();
    });
  });
</script>""", height=50)