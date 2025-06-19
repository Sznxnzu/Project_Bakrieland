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
st.markdown(
    """
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

  /* CAMERA CONTAINER STYLING */
  div[data-testid="stCameraInput"] {
    position: relative;
    width: var(--frame-size) !important;
    height: var(--frame-size) !important;
    margin: auto;
    background: var(--bg-circle);
    border-radius: 50%;
    overflow: hidden;
  }

  /* RING UNDERLAY */
  div[data-testid="stCameraInput"]::before {
    content: "";
    position: absolute;
    top: -8px; left: -8px;
    width: calc(100% + 16px);
    height: calc(100% + 16px);
    border-radius: 50%;
    background: conic-gradient(
      from 0deg,
      transparent 0deg 40deg,
      var(--cyan) 40deg 55deg,
      transparent 55deg 120deg,
      var(--cyan) 120deg 135deg,
      transparent 135deg 360deg
    );
    box-shadow: 0 0 20px var(--glow);
    pointer-events: none;
    z-index: 1;
  }

  /* THIN BORDER */
  div[data-testid="stCameraInput"]::after {
    content: "";
    position: absolute;
    top: -4px; left: -4px;
    width: calc(100% + 8px);
    height: calc(100% + 8px);
    border-radius: 50%;
    border: 2px solid var(--border);
    pointer-events: none;
    z-index: 1;
  }

  /* VIDEO & SNAPSHOT IMAGE */
  div[data-testid="stCameraInput"] video,
  div[data-testid="stCameraInput"] img {
    position: absolute;
    top: 0; left: 0;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover;
    border-radius: 50% !important;
    z-index: 2;
  }

  /* BUTTONS INSIDE FRAME */
  div[data-testid="stCameraInput"] button {
    position: absolute;
    bottom: 15px;
    left: 50%;
    transform: translateX(-50%);
    background-color: var(--cyan) !important;
    color: #000 !important;
    font-weight: 600;
    border-radius: 8px;
    padding: 8px 16px;
    z-index: 3;
    box-shadow: 0 0 10px var(--glow) !important;
  }

  /* HIDE DEFAULT CARD STYLE */
  div[data-testid="stFileUploader"],
  div[data-testid="stCameraInput"] > div {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
  }

  /* OTHER COMPONENT STYLES (UNCHANGED) */
  .header-box { /* ... */ }
  .portrait-box { /* ... */ }
  .mood-box-content { /* ... */ }
  .column-wrapper, .logo-box, .mascot-box { /* ... */ }

  /* RESPONSIVE */
  @media (max-width: 768px) {
    div[data-testid="stCameraInput"] {
      width: 80vw !important;
      height: 80vw !important;
      margin-top: 90px;
    }
    div[data-testid="stCameraInput"]::before {
      top: -6px; left: -6px;
      width: calc(100% + 12px);
      height: calc(100% + 12px);
    }
    div[data-testid="stCameraInput"]::after {
      top: -3px; left: -3px;
      width: calc(100% + 6px);
      height: calc(100% + 6px);
    }
  }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURE AI ---
try:
    genai.configure(api_key=st.secrets["gemini_api"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Error configuring Generative AI: {e}")
    st.stop()

# --- PLACEHOLDERS & SESSION STATE ---
placeholder_url = (
    "https://raw.githubusercontent.com/Sznxnzu/"
    "Project_Bakrieland/main/resources/other/placeholder.png"
)
placeholder_caption = ""
placeholder_analysis = (
    "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati "
    "dan mendapatkan rekomendasi yang dipersonalisasi."
)
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = placeholder_analysis
    st.session_state.image_urls = [placeholder_url] * 4
    st.session_state.image_captions = [placeholder_caption] * 4
    st.session_state.last_photo = None

# --- LAYOUT & LOGIC ---
row1 = st.container()
with row1:
    colA1, colA2, colA3 = st.columns([0.2, 0.6, 0.2])
    with colA1:
        st.markdown(
            """
            <div class="column-wrapper">
              <div class="logo-box">
                <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/35thn_logo.png" />
              </div>
              <div class="mascot-box">
                <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/mascot_logo.png" />
              </div>
            </div>
            """, unsafe_allow_html=True
        )
    with colA2:
        user_input = st.camera_input("", label_visibility="collapsed", key="camera")

        if user_input is not None and user_input != st.session_state.last_photo:
            st.session_state.last_photo = user_input
            with st.spinner("Menganalisis suasana hati Anda..."):
                try:
                    img = Image.open(io.BytesIO(user_input.getvalue()))
                    prompt_txt = requests.get(
                        "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt.txt"
                    ).text
                    json_txt = requests.get(
                        "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt_json.txt"
                    ).text

                    raw_output = model.generate_content([prompt_txt, img]).text
                    filenames = model.generate_content([json_txt, raw_output]).text.strip().split(",")

                    if len(filenames) >= 4:
                        mid = len(filenames) // 2
                        first, second = filenames[:mid], filenames[mid:]
                        # random rename & session_state update
                        first_targets = ["Bogor Nirwana Residence","Kahuripan Nirwana","Sayana Bogor","Taman Rasuna Epicentrum","The Masterpiece & The Empyreal"]
                        first_edit = [f+" "+str(random.randint(1,2)) if f.strip() in first_targets else f.strip() for f in first]
                        second_targets = ["Aston Bogor","Bagus Beach Walk","Grand ELTY Krakatoa","Hotel Aston Sidoarjo","Jungleland","Junglesea Kalianda","Rivera","Swiss Belresidences Rasuna Epicentrum","The Alana Malioboro","The Grove Suites","The Jungle Waterpark"]
                        second_edit = [f+" "+str(random.randint(1,2)) if f.strip() in second_targets else f.strip() for f in second]
                        st.session_state.image_urls = [
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{first_edit[0].strip()}.jpg",
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{first_edit[1].strip()}.jpg",
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{second_edit[0].strip()}.jpg",
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{second_edit[1].strip()}.jpg"
                        ]
                        st.session_state.image_captions = [first[0].strip(),first[1].strip(),second[0].strip(),second[1].strip()]
                        st.session_state.analysis_result = raw_output
                    else:
                        st.session_state.analysis_result = "Gagal memproses rekomendasi gambar. Silakan coba lagi."
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
                    st.session_state.analysis_result = "Terjadi kesalahan saat pemrosesan."
            st.rerun()
        elif user_input is None and st.session_state.last_photo:
            st.session_state.analysis_result = placeholder_analysis
            st.session_state.image_urls = [placeholder_url]*4
            st.session_state.image_captions = [placeholder_caption]*4
            st.session_state.last_photo = None
            st.rerun()
    with colA3:
        st.markdown(
            """
            <div>
              <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png" style="height:70px; margin-bottom:4px;" />
            </div>
            <div>
              <span>POWERED BY:</span>
              <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png" style="height:40px; margin:0 8px;" />
              <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png" style="height:40px;" />
            </div>
            """, unsafe_allow_html=True
        )

row2 = st.container()
with row2:
    escaped = html.escape(st.session_state.analysis_result)
    st.markdown(f"""
    <div class="mood-box-content">
      <h2>Mood Analytic</h2>
      <pre>{escaped}</pre>
    </div>
    """, unsafe_allow_html=True)

row3 = st.container()
with row3:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""
          <div class="portrait-box">
            <img src="{st.session_state.image_urls[0]}" />
            <p>{st.session_state.image_captions[0]}</p>
            <img src="{st.session_state.image_urls[1]}" />
            <p>{st.session_state.image_captions[1]}</p>
          </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""
          <div class="portrait-box">
            <img src="{st.session_state.image_urls[2]}" />
            <p>{st.session_state.image_captions[2]}</p>
            <img src="{st.session_state.image_urls[3]}" />
            <p>{st.session_state.image_captions[3]}</p>
          </div>
        """, unsafe_allow_html=True)

components.html(
    """
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
    """, height=100
)
