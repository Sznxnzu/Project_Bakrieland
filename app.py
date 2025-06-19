import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io, requests, html, random

# --- PAGE CONFIG ---
st.set_page_config(
    layout="wide",
    page_title="Bakrieland Mood Analytic",
    initial_sidebar_state="collapsed"
)

# --- INJECT CSS ---
st.markdown("""
<style>
  :root {
    --frame-size: 500px;
    --cyan: #00ffff;
    --glow: rgba(0,255,255,0.6);
    --border: rgba(0,255,255,0.8);
    --bg-circle: radial-gradient(circle at center, rgba(25,48,127,1) 0%, rgba(25,48,127,0.8) 70%, transparent 100%);
  }

  /* GLOBAL BACKGROUND */
  html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #19307f !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
  }
  ::-webkit-scrollbar { display: none; }

  /* HEADER BOX */
  .header-box {
    text-align: center;
    border: 2px solid var(--cyan);
    background-color: rgba(0,0,50,0.5);
    border-radius: 8px;
    padding: 6px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px var(--cyan);
    color: var(--cyan);
    font-size: 25px;
    font-family: 'Orbitron', sans-serif;
    letter-spacing: 1px;
  }

  /* PORTRAIT BOX */
  .portrait-box {
    border: 2px solid var(--cyan);
    background-color: rgba(0,0,30,0.6);
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px var(--cyan);
    text-align: center;
  }
  .portrait-box img {
    width: 100%;
    height: 200px;
    border-radius: 8px;
    object-fit: cover;
  }
  .portrait-box p {
    margin-top: 5px;
    font-size: 30px;
    color: #ccc;
    text-align: center;
  }

  /* MOOD CONTENT */
  .mood-box-content {
    border: 2px solid var(--cyan);
    background-color: rgba(10,15,30,0.85);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 20px var(--cyan);
    font-size: 25px;
    margin: 10px 0;
    transition: all 0.3s ease-in-out;
  }
  .mood-box-content:hover {
    box-shadow: 0 0 25px var(--cyan), 0 0 50px var(--cyan);
  }
  .mood-box-content h2 {
    font-size: 45px;
    margin-bottom: 0.5em;
  }
  .mood-box-content pre {
    margin: 0;
    white-space: pre-wrap;
    font-family: inherit;
  }

  /* SIDEBAR LOGOS */
  .column-wrapper {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 400px;
  }
  .logo-box {
    width: 150px;
    margin: 0 auto;
  }
  .logo-box img {
    width: 100%;
    border-radius: 8px;
  }
  .mascot-box {
    width: 150px;
    height: 200px;
    margin: 0 auto 20px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
  }
  .mascot-box img {
    width: 100%;
    border-radius: 8px;
  }

  /* OVERRIDE CAMERA INPUT */
  div[data-testid="stFileUploader"],
  div[data-testid="stCameraInput"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
  }
  div[data-testid="stCameraInput"] > div {
    background: transparent !important;
    box-shadow: none !important;
    border: none !important;
  }

  /* CAMERA FRAME & BACKGROUND CIRCLE */
  div[data-testid="stCameraInputWebcamStyledBox"] {
    position: relative;
    width: var(--frame-size) !important;
    height: var(--frame-size) !important;
    margin: auto;
    background: var(--bg-circle);
    border-radius: 50%;
    overflow: hidden;
  }
  div[data-testid="stCameraInputWebcamStyledBox"]::before {
    content: "";
    position: absolute;
    top: -8px; left: -8px;
    width: calc(100% + 16px);
    height: calc(100% + 16px);
    border-radius: 50%;
    background: repeating-conic-gradient(
      from 0deg,
      var(--cyan) 0deg 18deg,
      transparent 18deg 36deg
    );
    box-shadow: 0 0 20px var(--glow);
    pointer-events: none;
    z-index: 2;
  }
  div[data-testid="stCameraInputWebcamStyledBox"]::after {
    content: "";
    position: absolute;
    top: -4px; left: -4px;
    width: calc(100% + 8px);
    height: calc(100% + 8px);
    border-radius: 50%;
    border: 2px solid var(--border);
    pointer-events: none;
    z-index: 3;
  }
  div[data-testid="stCameraInputWebcamStyledBox"] video,
  div[data-testid="stCameraInputWebcamStyledBox"] img {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover;
    border-radius: 50% !important;
    box-shadow: 0 0 20px var(--glow);
  }
  [data-testid="stCameraInputSwitchButton"] { display: none !important; }

  /* RESPONSIVE MOBILE */
  @media (max-width: 768px) {
    .logo-box, .mascot-box { width: 100px; }
    div[data-testid="stCameraInputWebcamStyledBox"] {
      width: 80vw !important;
      height: 80vw !important;
      margin-top: 90px;
    }
    div[data-testid="stCameraInputWebcamStyledBox"]::before {
      top: -6px; left: -6px;
      width: calc(100% + 12px);
      height: calc(100% + 12px);
    }
    div[data-testid="stCameraInputWebcamStyledBox"]::after {
      top: -3px; left: -3px;
      width: calc(100% + 6px);
      height: calc(100% + 6px);
    }
  }
</style>
"""
