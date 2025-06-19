import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io, requests, html, random

st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# --- INJECT CSS SEKALI DI SINI ---
st.markdown("""
<style>
  :root {
    --frame-size: 500px;
    --cyan: #00ffff;
    --cyan-glow: rgba(0,255,255,0.6);
    --cyan-border: rgba(0,255,255,0.8);
  }

  html, body, [data-testid="stAppViewContainer"], .stApp {
    background-color: #19307f !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
  }
  ::-webkit-scrollbar { display: none; }

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

  .portrait-box {
    border: 2px solid var(--cyan);
    background-color: rgba(0,0,30,0.6);
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px var(--cyan);
    text-align: center;
  }

  .mood-box-content {
    border: 2px solid var(--cyan);
    background-color: rgba(10,15,30,0.85);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 20px var(--cyan);
    font-size: 25px;
    margin: 10px 0;
    width: 100%;
    transition: all 0.3s ease-in-out;
  }
  .mood-box-content:hover {
    box-shadow: 0 0 25px var(--cyan), 0 0 50px var(--cyan);
  }
  .mood-box-content h2 {
    font-size: 45px;
    margin-bottom: 0.5em;
  }
  .mood-box-content p,
  .mood-box-content ul {
    margin: 0 0 1em;
    padding-left: 20px;
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

  /* camera centering + overlay */
  .camera-container {
    display: flex;
    justify-content: center;
  }
  .camera-wrapper {
    position: relative;
    width: var(--frame-size);
    height: var(--frame-size);
  }
  .camera-wrapper::before {
    content: "";
    position: absolute;
    top: -8px; left: -8px;
    width: calc(100% + 16px);
    height: calc(100% + 16px);
    border-radius: 50%;
    background: conic-gradient(
      from 90deg,
      transparent 0deg 40deg,
      var(--cyan) 40deg 55deg,
      transparent 55deg 120deg,
      var(--cyan) 120deg 135deg,
      transparent 135deg 360deg
    );
    box-shadow: 0 0 20px var(--cyan-glow);
    pointer-events: none;
    z-index: 2;
  }
  .camera-wrapper::after {
    content: "";
    position: absolute;
    top: -4px; left: -4px;
    width: calc(100% + 8px);
    height: calc(100% + 8px);
    border-radius: 50%;
    border: 2px solid var(--cyan-border);
    pointer-events: none;
    z-index: 3;
  }

  /* Streamlit camera styling */
  div[data-testid="stCameraInput"] {
    width: 100% !important;
    height: 100% !important;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  div[data-testid="stCameraInputWebcamStyledBox"],
  div[data-testid="stCameraInput"] img,
  div[data-testid="stCameraInput"] video {
    width: 100% !important;
    height: 100% !important;
    border-radius: 50% !important;
    object-fit: cover;
    box-shadow: 0 0 20px var(--cyan-glow);
  }
  div[data-testid="stCameraInput"] button {
    position: absolute;
    bottom: 0; right: 0;
    background-color: #00c0cc;
    color: #000;
    font-weight: 600;
    font-size: 16px;
    border: none;
    border-radius: 8px;
    box-shadow: 0 4px 12px var(--cyan-glow);
    cursor: pointer;
    transition: all 0.2s ease-in-out;
    width: 150px;
    z-index: 4;
  }
  div[data-testid="stCameraInput"] button:hover {
    background-color: #00aabb;
    transform: scale(1.05);
    box-shadow: 0 6px 16px var(--cyan-glow);
  }
  [data-testid="stCameraInputSwitchButton"] {
    display: none !important;
  }

  @media (max-width: 768px) {
    .column-wrapper {
      flex-direction: row;
      justify-content: space-around;
      align-items: center;
      margin-bottom: 20px;
      height: auto;
    }
    .logo-box, .mascot-box {
      width: 100px;
    }
    img[src*="bakrieland_logo"] {
      height: 50px !important;
    }
    img[src*="google_logo"],
    img[src*="metrodata_logo"] {
      height: 30px !important;
    }
    .camera-wrapper {
      width: 80vw;
      height: 80vw;
      margin-top: 90px;
    }
    div[data-testid="stCameraInput"],
    div[data-testid="stCameraInputWebcamStyledBox"],
    div[data-testid="stCameraInput"] img {
      width: 80vw !important;
      height: 80vw !important;
      max-width: 300px !important;
      max-height: 300px !important;
    }
    div[data-testid="stCameraInput"] button {
      width: 120px;
      font-size: 14px;
      bottom: 10px;
      right: 50%;
      transform: translateX(50%);
    }
  }
</style>
""", unsafe_allow_html=True)

# --- LOGIC & LAYOUT ---
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

row1 = st.container()
with row1:
    colA1, colA2, colA3 = st.columns([0.2, 0.6, 0.2])
    with colA1:
        st.markdown("""
        <div class="column-wrapper">
          <div class="logo-box">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/35thn_logo.png"/>
          </div>
          <div class="mascot-box">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/mascot_logo.png"/>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with colA2:
        # Bungkus dengan container + wrapper
        st.markdown(
            '<div class="camera-container"><div class="camera-wrapper">',
            unsafe_allow_html=True
        )
        user_input = st.camera_input("", label_visibility="collapsed", key="camera")
        st.markdown('</div></div>', unsafe_allow_html=True)

        if user_input is not None and user_input != st.session_state.last_photo:
            st.session_state.last_photo = user_input
            with st.spinner("Menganalisis suasana hati Anda..."):
                try:
                    img = Image.open(io.BytesIO(user_input.getvalue())).convert("RGBA")
                    # generate analysis
                    prompt_txt = requests.get(
                        "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt.txt"
                    ).text
                    json_txt = requests.get(
                        "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt_json.txt"
                    ).text

                    raw_out = model.generate_content([prompt_txt, img]).text
                    filenames = model.generate_content([json_txt, raw_out]).text.strip().split(",")

                    if len(filenames) >= 4:
                        mid = len(filenames)//2
                        first, second = filenames[:mid], filenames[mid:]
                        # random rename logic
                        # ... (sama seperti sebelumnya) ...
                        # simpan ke session_state
                    else:
                        st.session_state.analysis_result = "Gagal memproses rekomendasi gambar. Silakan coba lagi."
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
                    st.session_state.analysis_result = "Terjadi kesalahan saat pemrosesan."
            st.rerun()
        elif user_input is None and st.session_state.last_photo is not None:
            st.session_state.analysis_result = placeholder_analysis
            st.session_state.image_urls = [placeholder_url]*4
            st.session_state.image_captions = [placeholder_caption]*4
            st.session_state.last_photo = None
            st.rerun()

    with colA3:
        st.markdown("""
        <div>
          <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png" style="height:70px; margin-bottom:4px;"/>
        </div>
        <div>
          <span>POWERED BY:</span>
          <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png" style="height:40px; margin:0 8px;"/>
          <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png" style="height:40px;"/>
        </div>
        """, unsafe_allow_html=True)

row2 = st.container()
with row2:
    escaped = html.escape(st.session_state.analysis_result)
    st.markdown(f"""
    <div class="mood-box-content">
      <h2>Mood Analytic</h2>
      <pre style="white-space:pre-wrap; font-family:inherit;">{escaped}</pre>
    </div>
    """, unsafe_allow_html=True)

row3 = st.container()
with row3:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""
          <div class="portrait-box">
            <img src="{st.session_state.image_urls[0]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;"/>
            <p style="font-size:30px; color:#ccc;">{st.session_state.image_captions[0]}</p>
            <img src="{st.session_state.image_urls[1]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;"/>
            <p style="font-size:30px; color:#ccc;">{st.session_state.image_captions[1]}</p>
          </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""
          <div class="portrait-box">
            <img src="{st.session_state.image_urls[2]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;"/>
            <p style="font-size:30px; color:#ccc;">{st.session_state.image_captions[2]}</p>
            <img src="{st.session_state.image_urls[3]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;"/>
            <p style="font-size:30px; color:#ccc;">{st.session_state.image_captions[3]}</p>
          </div>
        """, unsafe_allow_html=True)

components.html("""
<html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  </head>
  <body>
    <button id="screenshotBtn" style="
        position: fixed; bottom:20px; right:20px; z-index:9999;
        background-color:#00c0cc; color:white; border:none;
        padding:10px 20px; font-size:16px; border-radius:8px;
        box-shadow:0 4px 12px rgba(0,240,255,0.6); cursor:pointer;
    ">📸 Screenshot</button>
    <script>
      document.getElementById("screenshotBtn").addEventListener("click", function(){
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
