import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html

# --- Page layout ---
st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")
# --- Background matrix effect (canvas) ---
components.html("""
<canvas id="matrix-canvas" style="
    position: fixed;
    top: 0;
    left: 0;
    z-index: -10;
    width: 100vw;
    height: 100vh;
    opacity: 0.25;
    background: black;
    pointer-events: none;"></canvas>

<script>
const c = document.getElementById("matrix-canvas");
const ctx = c.getContext("2d");
c.height = window.innerHeight;
c.width = window.innerWidth;

const letters = "01";
const fontSize = 14;
const columns = c.width / fontSize;
const drops = Array(Math.floor(columns)).fill(1);

function draw() {
  ctx.fillStyle = "rgba(0, 0, 0, 0.05)";
  ctx.fillRect(0, 0, c.width, c.height);
  ctx.fillStyle = "#00FF00";
  ctx.font = fontSize + "px monospace";

  for (let i = 0; i < drops.length; i++) {
    const text = letters.charAt(Math.floor(Math.random() * letters.length));
    ctx.fillText(text, i * fontSize, drops[i] * fontSize);
    if (drops[i] * fontSize > c.height && Math.random() > 0.975) {
      drops[i] = 0;
    }
    drops[i]++;
  }
}
setInterval(draw, 33);
</script>
""", height=0)
# --- Styling ---
st.markdown("""
<style>
html, body {
    background: black !important;
    overflow: hidden !important;
}
[data-testid="stAppViewContainer"] {
    overflow: hidden !important;
}
::-webkit-scrollbar { display: none; }
.stApp {
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
.mood-box, .mood-box-content {
    border: 2px solid #00f0ff;
    background-color: rgba(10, 15, 30, 0.85);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 20px #00f0ff;
    font-size: 10px;
    margin-top: 10px;
    width: 100%;
}
.mood-box { height: 17vh; }
div[data-testid="stCameraInput"] > div {
    aspect-ratio: 4 / 5;
    width: 60% !important;
    height: auto !important;
    margin: 0;
    border-radius: 20px;
    background-color: rgba(0, 0, 0, 0.1);
}
div[data-testid="stCameraInput"] button {
    display: inline-block !important;
    visibility: visible !important;
    position: relative !important;
    z-index: 10 !important;
}
div[data-testid="stCameraInput"] video,
div[data-testid="stCameraInput"] img {
    object-fit: cover;
    width: 100%;
    height: 100%;
    border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- Gemini model setup ---
genai.configure(api_key=st.secrets["gemini_api"])
model = genai.GenerativeModel("models/gemini-2.5-flash-preview-04-17-thinking")

# --- UI ---
col_header_left, col_header_right = st.columns([0.85, 0.15])
with col_header_right:
    col_00, col_01 = st.columns([0.3, 0.7])
    with col_00:
        st.markdown("""
        <div style='display: flex; align-items: flex-end; height: 100%; justify-content: flex-start;'>
            <p style='font-size: 0.6em; color:#aaa; margin: 0;'>POWERED BY</p>
        </div>
        """, unsafe_allow_html=True)
    with col_01:
        st.markdown("""
        <div style='text-align: right;'>
            <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png' width='120' margin: 5px;'>
            <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png' width='50' style='margin: 5px;'>
            <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png' width='50' style='margin: 5px;'>
        </div>
        """, unsafe_allow_html=True)

    components.html("""
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <div style="display: flex; justify-content: center; align-items: center;">
        <lottie-player 
            id="robot"
            src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/Animation%20-%201749118794076.json"
            background="transparent"
            speed="1"
            style="width: 300px; height: 300px;"
            autoplay
            loop>
        </lottie-player>
    </div>
    """, height=340)

    st.markdown("""
          <div class="qr-box">
              <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/qr_logo.png" style="width:100%; border-radius: 8px;" />
          </div>
        """, unsafe_allow_html=True)

# -- (lanjutkan bagian rekomendasi, kamera, dan analisa sesuai struktur kamu) --
