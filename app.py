import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import random

st.set_page_config(
    layout="wide",
    page_title="Bakrieland Mood Analytic",
    initial_sidebar_state="collapsed"
)

# --- CSS STYLES ---
st.markdown("""
<style>
/* Global background */
html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #19307f !important;
    background: none !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}
::-webkit-scrollbar { display: none; }

/* Header boxes */
.header-box { /* unchanged */ }
.portrait-box { /* unchanged */ }
.column-wrapper { /* unchanged */ }
.thirtyfive-thn-box, .mascot-box { /* unchanged */ }
.mood-box-content { /* unchanged */ }
.mood-box-content:hover { /* unchanged */ }
.mood-box-content p, .mood-box-content h2, .mood-box-content ul { /* unchanged */ }

/* === Camera Input Overrides === */
div[data-testid="stCameraInput"] {
  position: relative !important;
  width: 60% !important;
  max-width: 400px !important;
  margin: 0 auto !important;
  margin-bottom: 80px !important;  /* space for button */
  overflow: visible !important;     /* allow button to show */
  background: transparent !important;
}

div[data-testid="stCameraInput"] > div:first-child {
  /* disable default clipping */
  overflow: visible !important;
}

/* clip the video itself into a circle */
div[data-testid="stCameraInput"] video,
div[data-testid="stCameraInput"] img {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  clip-path: circle(50% at 50% 50%) !important;
  -webkit-clip-path: circle(50% at 50% 50%) !important;
  position: relative;
  z-index: 1;
}

/* overlay PNG frame */
div[data-testid="stCameraInput"]::before {
  content: "";
  position: absolute;
  top: -13%; left: -18%;
  width: 140%; height: 123%;
  background: url("https://raw.githubusercontent.com/husnanali05/FP_Datmin/main/Halaman%20Story%20WA%20(1).png") center/contain no-repeat !important;
  pointer-events: none;
  z-index: 2;
}

/* move button below the circle */
div[data-testid="stCameraInput"] button {
  position: absolute !important;
  bottom: -50px !important;
  left: 50% !important;
  transform: translateX(-50%) !important;
  background: linear-gradient(135deg, #00c0cc, #006f8e) !important;
  color: #fff !important;
  font-size: 16px !important;
  font-weight: 600 !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 8px 16px !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
  cursor: pointer !important;
  transition: transform .2s, box-shadow .2s !important;
  z-index: 3 !important;
}

div[data-testid="stCameraInput"] button:hover {
  transform: translateX(-50%) scale(1.05) !important;
  box-shadow: 0 6px 18px rgba(0,0,0,0.3) !important;
}

/* hide switch button */
[data-testid="stCameraInputSwitchButton"] { display: none !important; }

/* mobile tweaks */
@media (max-width: 768px) {
  div[data-testid="stCameraInput"] {
    width: 80% !important;
    max-width: 300px !important;
    margin-bottom: 60px !important;
  }
  div[data-testid="stCameraInput"] button {
    bottom: -40px !important;
    width: 120px !important;
    font-size: 14px !important;
  }
}
</style>
""", unsafe_allow_html=True)

# --- Logic & Layout ---
try:
    genai.configure(api_key=st.secrets["gemini_api"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Error configuring AI: {e}")
    st.stop()

placeholder_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"
placeholder_caption = ""
placeholder_analysis = (
    "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati "
    "dan mendapatkan rekomendasi yang dipersonalisasi."
)

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = placeholder_analysis
    st.session_state.image_urls = [placeholder_url]*4
    st.session_state.image_captions = [placeholder_caption]*4
    st.session_state.last_photo = None

row1 = st.container()
with row1:
    colA1, colA2, colA3 = st.columns([0.2,0.6,0.2])
    with colA1:
        st.markdown(
            '<div class="column-wrapper">'
            '<div class="thirtyfive-thn-box"><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/35thn_logo.png"/></div>'
            '<div class="mascot-box"><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/mascot_logo.png"/></div>'
            '</div>', unsafe_allow_html=True)
    with colA2:
        user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")
        # ... rest of your camera logic unchanged ...
    with colA3:
        st.markdown(
            '<div><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png" style="height:70px;"/></div>'
            '<div>POWERED BY:</div>'
            '<div><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png" style="height:40px; margin-right:-20px;"/>'
            '<img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png" style="height:40px;"/></div>',
            unsafe_allow_html=True)
# ... remaining layout & recommendation sections remain unchanged ...

# Screenshot component unchanged
components.html(
    """
<html><head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
</head><body>
<button id="screenshotBtn" style="position:fixed;bottom:20px;right:20px;border:none;padding:10px;border-radius:8px;background:#00c0cc;color:#fff;cursor:pointer;z-index:9999;">📸 Screenshot</button>
<script>document.getElementById('screenshotBtn').onclick=()=>{html2canvas(parent.document.body).then(c=>{let a=document.createElement('a');a.href=c.toDataURL();a.download='screenshot.png';a.click();});};</script>
</body></html>
    """, height=100)
