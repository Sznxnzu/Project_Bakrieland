import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import random

st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# --- CSS STYLES ---
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: none !important;
    background-color: #19307f !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}
::-webkit-scrollbar { display: none; }

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

.camera-wrapper {
  display: flex;
  justify-content: center;
}

.column-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 400px;
}

.35thn-box {
  width: 150px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.35thn-box img {
  width: 100%;
  border-radius: 8px;
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
  border-radius: 8px;
}

/* Kamera dalam lingkaran */
div[data-testid="stCameraInputWebcamStyledBox"] {
  width: 500px !important;
  height: 500px !important;
  border-radius: 50% !important;
  overflow: hidden;
  margin: auto;
  box-shadow: 0 0 20px rgba(0,240,255,0.5);
}

div[data-testid="stCameraInput"] img {
  object-fit: cover;
  aspect-ratio: 1 / 1;
  border-radius: 50% !important;
  width: 500px !important;
  height: 500px !important;
  box-shadow: 0 0 20px rgba(0,240,255,0.5);
}

.mood-box-content {
    border: 2px solid #00f0ff;
    background-color: rgba(10, 15, 30, 0.85);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 20px #00f0ff;
    font-size: 25px;
    margin-top: 10px;
    margin-bottom: 10px;
    width: 100%;
    height: auto;
}
.mood-box-content h2 {
    font-size: 45px;
    color: #00f0ff;
    font-family: 'Orbitron', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# --- INIT STATE ---
try:
    genai.configure(api_key=st.secrets["gemini_api"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Error configuring Generative AI: {e}")
    st.stop()

placeholder_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"
placeholder_caption = ""
placeholder_analysis = "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati dan mendapatkan rekomendasi yang dipersonalisasi."

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = placeholder_analysis
    st.session_state.image_urls = [placeholder_url] * 4
    st.session_state.image_captions = [placeholder_caption] * 4
    st.session_state.last_photo = None

# --- LAYOUT ---
colA1, colA2, colA3 = st.columns([0.2, 0.6, 0.2])

with colA1:
    st.markdown("""
    <div class="column-wrapper">
      <div class="35thn-box">
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

with colA3:
    st.markdown("""
    <div style="text-align: right;">
      <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png"
           style="height: 50px;" />
      <div style="font-size: 12px; color: white;">POWERED BY:</div>
      <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png"
           style="height: 28px;" />
      <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png"
           style="height: 28px;" />
    </div>
    """, unsafe_allow_html=True)

# --- ANALYSIS RESULT ---
escaped_analysis = html.escape(st.session_state.analysis_result)
st.markdown(f"""
<div class="mood-box-content">
  <h2>Mood Analytic</h2>
  <pre style="white-space: pre-wrap; font-family: inherit; color:white">{escaped_analysis}</pre>
</div>
""", unsafe_allow_html=True)
