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

.responsive-wrapper {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
}

.logo-35 {
  position: absolute;
  top: 10px;
  left: 10px;
  width: 70px;
}

.maskot-rusa {
  position: absolute;
  top: 140px;
  left: 10px;
  width: 70px;
}

.kamera-wrapper {
  z-index: 1;
}

.powered-right {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  z-index: 2;
}

.powered-text {
  font-size: 12px;
  color: white;
  margin-bottom: 2px;
}

.powered-logo img {
  height: 28px;
  margin-left: 4px;
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
st.markdown("""
<div class="responsive-wrapper">
    <img class="logo-35" src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/35thn_logo.png" />
    <img class="maskot-rusa" src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/mascot_logo.png" />
    <div class="kamera-wrapper">
""", unsafe_allow_html=True)

user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")

st.markdown("""
    </div>
    <div class="powered-right">
        <img class="logo-bakrieland" src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png" />
        <div class="powered-text">POWERED BY:</div>
        <div class="powered-logo">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png" />
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png" />
        </div>
    </div>
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
