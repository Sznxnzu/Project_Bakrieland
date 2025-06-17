import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import random

# Konfigurasi halaman, dibuat 'wide' untuk fleksibilitas di desktop
st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# --- CSS LENGKAP UNTUK DESKTOP DAN MOBILE (CANVAS) ---
st.markdown("""
<style>
/* --- Gaya Dasar & Latar Belakang --- */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: none !important;
    background-color: #19307f !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}
::-webkit-scrollbar {
  display: none;
}

/* Menghilangkan padding utama dari Streamlit untuk kontrol penuh */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* --- Gaya Elemen UI (Umum) --- */
.header-box {
    text-align: center;
    border: 2px solid #00f0ff;
    background-color: rgba(0,0,50,0.5);
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px #00f0ff;
    color: #00f0ff;
    font-size: 25px;
    font-family: 'Orbitron', sans-serif;
    letter-spacing: 1px;
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

/* --- TATA LETAK DESKTOP --- */

/* Wrapper untuk logo di sisi kiri desktop */
.desktop-side-logos {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 450px;
}
.desktop-side-logos .logo-box img {
  width: 150px;
  height: auto;
}

/* Wrapper untuk logo di sisi kanan desktop */
.desktop-poweredby {
    text-align: right;
}
.desktop-poweredby img {
    height: 70px;
    margin-bottom: 15px;
}
.desktop-poweredby .powered-by-text {
    color: white;
    font-size: 16px;
}
.desktop-poweredby .powered-by-logos img {
    height: 40px;
    vertical-align: middle;
}

/* Kamera untuk Desktop */
div[data-testid="stCameraInput"] {
  width: 450px !important;
  height: 450px !important;
  margin: 0 auto;
}
div[data-testid="stCameraInputWebcamStyledBox"], div[data-testid="stCameraInput"] video, div[data-testid="stCameraInput"] img {
  width: 450px !important;
  height: 450px !important;
  border-radius: 50% !important;
  object-fit: cover;
}
div[data-testid="stCameraInput"] button {
    width: 150px;
    position: absolute;
    bottom: 20px;
    right: 20px;
}


/* --- TATA LETAK MOBILE (CANVAS VIEW) --- */
@media (max-width: 768px) {
    /* Sembunyikan elemen khusus desktop */
    .desktop-side-logos, .desktop-poweredby, [data-testid="stHorizontalBlock"] > div:nth-child(1), [data-testid="stHorizontalBlock"] > div:nth-child(3) {
        display: none !important;
    }
    
    .block-container {
        padding-top: 1rem !important;
    }

    /* Kontainer utama untuk semua elemen di mobile */
    .mobile-canvas-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    /* 1. Header dengan semua logo */
    .mobile-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 95%;
        margin-bottom: 20px;
    }
    .mobile-header .left-logos {
        display: flex;
        align-items: center;
    }
    .mobile-header .left-logos img {
        height: 35px;
        margin-right: 8px;
    }
    .mobile-header .right-logo img {
        height: 40px;
    }
    
    /* 2. Kamera */
    .mobile-canvas-container div[data-testid="stCameraInput"],
    .mobile-canvas-container div[data-testid="stCameraInputWebcamStyledBox"],
    .mobile-canvas-container div[data-testid="stCameraInput"] video,
    .mobile-canvas-container div[data-testid="stCameraInput"] img {
        width: 220px !important;
        height: 220px !important;
        border-radius: 50% !important;
        object-fit: cover;
        margin: 0 auto;
    }
    .mobile-canvas-container div[data-testid="stCameraInput"] button {
        width: 120px;
        font-size: 14px;
        bottom: -40px; /* Posisi di bawah kamera */
        right: 50%;
        transform: translateX(50%);
    }

    /* 3. Powered By Logos */
    .mobile-poweredby {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 60px; /* Jarak dari bawah tombol kamera */
        margin-bottom: 20px;
    }
    .mobile-poweredby .powered-by-text {
        font-size: 12px;
        color: #ccc;
    }
    .mobile-poweredby .powered-by-logos {
        display: flex;
        align-items: center;
    }
    .mobile-poweredby .powered-by-logos img {
        height: 25px !important;
        margin: 0 5px;
    }
    
    /* 4. Mood Analytic Box */
    .mood-box-content {
        width: 95%;
        margin-left: auto;
        margin-right: auto;
    }
    .mood-box-content h2 { font-size: 22px; text-align: center; }
    .mood-box-content pre { font-size: 14px; text-align: center; }

    /* 5. Recommendation Boxes */
    .mobile-recommendations {
        width: 95%;
        margin-top: 10px;
    }
    .mobile-recommendations .header-box { font-size: 18px; }
    .mobile-recommendations .portrait-box img {
        max-height: 180px;
        width: 100%;
        object-fit: cover;
    }
    .mobile-recommendations .portrait-box p { font-size: 18px; }

    /* 6. Tombol QR Code / Screenshot */
    #screenshotBtn {
        font-size: 12px !important;
        padding: 8px 15px !important;
    }
}
</style>
""", unsafe_allow_html=True)


# --- State Management ---
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati."
    st.session_state.image_urls = ["https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"] * 4
    st.session_state.image_captions = [""] * 4
    st.session_state.last_photo = None

# --- Image Processing Logic ---
def process_image(user_input_bytes):
    with st.spinner("Menganalisis suasana hati Anda..."):
        try:
            image = Image.open(io.BytesIO(user_input_bytes.getvalue()))
            
            # Fetch prompts (disarankan untuk ditaruh di cache jika memungkinkan)
            prompt_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt.txt"
            analysis_prompt = requests.get(prompt_url).text
            
            json_prompt_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt_json.txt"
            json_prompt = requests.get(json_prompt_url).text

            # Generate analysis and recommendations
            model = genai.GenerativeModel("gemini-1.5-flash")
            analysis_response = model.generate_content([analysis_prompt, image])
            raw_output = analysis_response.text
            
            json_response = model.generate_content([json_prompt, raw_output])
            filenames = json_response.text.strip().split(",")

            if len(filenames) >= 4:
                # Update analysis result
                st.session_state.analysis_result = raw_output

                # Update recommendations
                # (Logika untuk memilih nama file acak tetap sama)
                first_filenames = filenames[:2]
                second_filenames = filenames[2:4]
                st.session_state.image_urls = [
                    f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{first_filenames[0].strip()}.jpg",
                    f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{first_filenames[1].strip()}.jpg",
                    f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{second_filenames[0].strip()}.jpg",
                    f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{second_filenames[1].strip()}.jpg"
                ]
                st.session_state.image_captions = [name.strip() for name in filenames]
            else:
                st.session_state.analysis_result = "Gagal memproses rekomendasi. Silakan coba lagi."

        except Exception as e:
            st.error(f"Terjadi kesalahan saat pemrosesan: {e}")
            st.session_state.analysis_result = "Gagal menganalisis gambar. Silakan coba lagi."


# --- TATA LETAK APLIKASI ---

# --- Tampilan Desktop ---
desktop_cols = st.columns([0.2, 0.6, 0.2])

with desktop_cols[0]:
    st.markdown("""
    <div class="desktop-side-logos">
        <div class="logo-box"><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/35thn_logo.png"></div>
        <div class="logo-box"><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/mascot_logo.png"></div>
    </div>
    """, unsafe_allow_html=True)

with desktop_cols[1]:
    # Ini adalah area tengah yang akan digunakan oleh kedua tampilan
    # Wrapper mobile-canvas-container akan membungkus semua elemen di mobile
    st.markdown('<div class="mobile-canvas-container">', unsafe_allow_html=True)

    # 1. Header Mobile
    st.markdown("""
    <div class="mobile-header">
        <div class="left-logos">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/35thn_logo.png">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/mascot_logo.png">
        </div>
        <div class="right-logo">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png">
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Kamera (Shared)
    user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")

    # 3. Powered By (Mobile)
    st.markdown("""
    <div class="mobile-poweredby">
        <div class="powered-by-text">POWERED BY:</div>
        <div class="powered-by-logos">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 4. Mood Analytic (Shared)
    escaped_analysis = html.escape(st.session_state.analysis_result)
    st.markdown(f"""
    <div class="mood-box-content">
      <h2>Mood Analytic</h2>
      <pre style="white-space: pre-wrap; font-family: inherit;">{escaped_analysis}</pre>
    </div>
    """, unsafe_allow_html=True)

    # 5. Rekomendasi (Wrapper untuk Mobile)
    st.markdown('<div class="mobile-recommendations">', unsafe_allow_html=True)
    st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="portrait-box">
        <img src="{st.session_state.image_urls[0]}">
        <p>{st.session_state.image_captions[0]}</p>
        <img src="{st.session_state.image_urls[1]}">
        <p>{st.session_state.image_captions[1]}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="portrait-box">
        <img src="{st.session_state.image_urls[2]}">
        <p>{st.session_state.image_captions[2]}</p>
        <img src="{st.session_state.image_urls[3]}">
        <p>{st.session_state.image_captions[3]}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True) # Penutup mobile-recommendations

    st.markdown('</div>', unsafe_allow_html=True) # Penutup mobile-canvas-container

with desktop_cols[2]:
    st.markdown("""
    <div class="desktop-poweredby">
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png">
        <div class="powered-by-text">POWERED BY:</div>
        <div class="powered-by-logos">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png">
        </div>
    </div>
    """, unsafe_allow_html=True)

# Logika setelah layout selesai didefinisikan
if user_input is not None and user_input != st.session_state.last_photo:
    st.session_state.last_photo = user_input
    genai.configure(api_key=st.secrets["gemini_api"]) # Konfigurasi API saat dibutuhkan
    process_image(user_input)
    st.rerun()

elif user_input is None and st.session_state.last_photo is not None:
    # Reset jika kamera ditutup setelah foto diambil
    st.session_state.analysis_result = "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati."
    st.session_state.image_urls = ["https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"] * 4
    st.session_state.image_captions = [""] * 4
    st.session_state.last_photo = None
    st.rerun()


# --- Tombol Screenshot / QR Code ---
components.html("""
<html><body>
    <button id="screenshotBtn" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999; background-color: #00c0cc; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 8px; cursor: pointer; box-shadow: 0 4px 12px rgba(0, 240, 255, 0.6);">📸 QRCODE</button>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <script>
      document.getElementById("screenshotBtn").addEventListener("click", function () {
        const mainContent = parent.document.querySelector('.block-container');
        html2canvas(mainContent).then(canvas => {
          const link = document.createElement("a");
          link.download = "mood-analytic-bakrieland.png";
          link.href = canvas.toDataURL();
          link.click();
        });
      });
    </script>
</body></html>
""", height=100)