import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import random

st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# --- CSS STYLES (Tidak ada perubahan signifikan) ---
st.markdown("""
<style>
/* Gaya dasar dan tema */
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
.header-box {
    text-align: center;
    border: 2px solid #00f0ff;
    background-color: rgba(0,0,50,0.5);
    border-radius: 8px;
    padding: 6px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px #00f0ff;
    color: #00f0ff;
    font-size: 25px;
    font-family: 'Orbitron', sans-serif;
    letter-spacing: 1px;
}
.column-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 400px;
}
.logo-box {
  width: 150px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
.logo-box img {
  width: 100%;
  vertical-align: top;
}
.mascot-box {
  width: 150px;
  height: 200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  margin-bottom: 20px;
}
.mascot-box img {
  width: 100%;
}
.camera-wrapper {
  display: flex;
  justify-content: center;
}
div[data-testid="stCameraInput"] {
  width:500px !important;
  height: 500px !important;
  display: flex;
  flex-direction: column;
  margin: 0 auto;
  align-items: center;
  justify-content: center;
}
div[data-testid="stCameraInput"] div {
  background-color: transparent !important;
  flex: 0 0 auto;
  width: 100%;
  height: 100%;
  max-width: 500px;
}
div[data-testid="stCameraInputWebcamStyledBox"] {
  width: 500px !important;
  height: 500px !important;
  border-radius: 50% !important;
  overflow: hidden;
  margin: auto;
  box-shadow: 0 0 20px rgba(0,240,255,0.5);
}
div[data-testid="stCameraInput"] video {
  object-fit: cover;
  width: 100%;
  height: 100%;
  border-radius: 0;
}
div[data-testid="stCameraInput"] img {
  display: block;
  object-fit: cover;
  aspect-ratio: 1 / 1;
  width: 500px !important;
  height: 500px !important;
  border-radius: 50% !important;
  box-shadow: 0 0 20px rgba(0,240,255,0.5);
  margin: 0;
}

/* Responsive CSS */
@media (max-width: 768px) {
  .st-emotion-cache-z5fcl4 {
      flex-direction: column;
  }
  div[data-testid="stCameraInput"],
  div[data-testid="stCameraInput"] div,
  div[data-testid="stCameraInputWebcamStyledBox"],
  div[data-testid="stCameraInput"] img {
      width: 80vw !important;
      height: 80vw !important;
      max-width: 300px !important;
      max-height: 300px !important;
  }
  .column-wrapper {
      flex-direction: row;
      height: auto;
      align-items: center;
      justify-content: space-around;
      margin-bottom: 20px;
  }
  .logo-box, .mascot-box {
      width: 100px;
      height: auto;
      margin: 0;
  }
}
</style>
""", unsafe_allow_html=True)


# --- LOGIC (Tidak ada perubahan) ---
# Konfigurasi model AI
try:
    genai.configure(api_key=st.secrets["gemini_api"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Error configuring Generative AI: {e}")
    st.stop()

# Inisialisasi session state jika belum ada
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False
if "last_photo" not in st.session_state:
    st.session_state.last_photo = None


# --- LAYOUT APLIKASI ---

# Bagian Header dan Kamera (Tidak ada perubahan)
row1 = st.container()
with row1:
    colA1, colA2, colA3 = st.columns([0.2, 0.6, 0.2])
    with colA1:
        st.write("")
        st.markdown("""
        <div class="column-wrapper">
            <div class="logo-box">
                <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/35thn_logo.png" />
            </div>
            <div class="mascot-box">
                <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/mascot_logo.png" />
            </div>
        </div>
        """, unsafe_allow_html=True)
    with colA2:
        st.markdown('<div class="camera-wrapper">', unsafe_allow_html=True)
        user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")
        st.markdown('</div>', unsafe_allow_html=True)

        # Proses gambar dan set flag bahwa analisis selesai
        if user_input is not None and user_input != st.session_state.last_photo:
            st.session_state.last_photo = user_input
            with st.spinner("Menganalisis suasana hati Anda..."):
                # Di sini bisa ditambahkan logic untuk melakukan sesuatu,
                # tapi hasilnya tidak perlu disimpan karena akan menampilkan iframe
                # Contoh: time.sleep(2) # simulasi proses
                st.session_state.analysis_done = True
            st.rerun()

        elif user_input is None and st.session_state.last_photo is not None:
             st.session_state.last_photo = None
             st.session_state.analysis_done = False
             st.rerun()

    with colA3:
        # Kolom kanan untuk logo (tidak ada perubahan)
        st.markdown("""
        <div style="text-align: right; padding-top: 20px;">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png" style="height: 70px; margin-bottom: 25px;" />
            <br>
            <span>POWERED BY:</span>
            <br>
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png" style="height: 40px;" />
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png" style="height: 40px;" />
        </div>
        """, unsafe_allow_html=True)


# --- BAGIAN HASIL (DIGANTI DENGAN IFRAME CANVA) ---

# Tampilkan iframe Canva HANYA JIKA foto sudah diambil dan diproses
if st.session_state.analysis_done:
    st.markdown("---") # Garis pemisah
    st.header("Hasil Untuk Anda", anchor=False)

    # Kode Iframe dari Anda dimasukkan di sini menggunakan st.components.v1.html
    canva_embed_code = """
    <div style="position: relative; width: 100%; height: 0; padding-top: 177.7778%;
     padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden;
     border-radius: 8px; will-change: transform;">
      <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;"
        src="https://www.canva.com/design/DAGqnj9Nc3M/QvxgADQeoLuupzkhJaj1dA/view?embed" allowfullscreen="allowfullscreen" allow="fullscreen">
      </iframe>
    </div>
    <a href="https://www.canva.com/design/DAGqnj9Nc3M/QvxgADQeoLuupzkhJaj1dA/view?utm_content=DAGqnj9Nc3M&utm_campaign=designshare&utm_medium=embeds&utm_source=link" target="_blank" rel="noopener">Copy of Template </a> by Husnan Ali Husnain
    """
    # Menggunakan components.html untuk merender iframe. Tinggi (height) bisa disesuaikan.
    # Responsive div di dalam kode Anda akan mengatur tinggi iframe secara otomatis.
    components.html(canva_embed_code, height=800, scrolling=True)

else:
    # Pesan yang ditampilkan sebelum kamera digunakan
    st.info("Silakan ambil foto untuk menampilkan hasil.")


# Tombol screenshot (tidak ada perubahan)
components.html("""
<html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  </head>
  <body>
    <button id="screenshotBtn" style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        background-color: #00c0cc;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 8px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 240, 255, 0.6);
    ">📸 Screenshot</button>

    <script>
      document.getElementById("screenshotBtn").addEventListener("click", function () {
        html2canvas(parent.document.body).then(canvas => {
          const link = document.createElement("a");
          link.download = "screenshot.png";
          link.href = canvas.toDataURL();
          link.click();
        });
      });
    </script>
  </body>
</html>
""", height=100)