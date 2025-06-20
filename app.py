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

.portrait-box {
    border: 2px solid #00f0ff;
    background-color: rgba(0,0,30,0.6);
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px #00f0ff;
    text-align: center;
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
    transition: all 0.3s ease-in-out;
}
.mood-box-content:hover {
    box-shadow: 0 0 25px #00f0ff, 0 0 50px #00f0ff;
}
.mood-box-content p {
    margin-bottom: 0;
}
.mood-box-content h2{
    font-size: 45px
}
.mood-box-content ul {
    margin-top: 0;
    margin-bottom: 1em;
    padding-left: 20px;
}
.camera-wrapper {
  position: relative;       
  display: inline-block;    
  width: 80vw;              
  max-width: 500px;
  aspect-ratio: 1;          
}
.camera-frame {
  position: absolute;
  width: 750px !important;
  height: 750px !important;
  top: -110px !important;
  left: -35px !important;
  background-image: url("https://raw.githubusercontent.com/husnanali05/FP_Datmin/main/Halaman%20Story%20WA%20(1).png");
  background-size: contain;
  background-repeat: no-repeat;
  background-position: center;
  z-index: 3;
}

/* Kamera style desktop */
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

div[data-testid="stCameraInput"] button {
  z-index: 10;
  position: absolute;
  bottom: 0;
  right: 0;
  background-color: #00c0cc;
  color: #000;
  font-weight: 600;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 240, 255, 0.6);
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  width: 150px;
}

div[data-testid="stCameraInput"] button:hover {
  background-color: #00aabb;
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 240, 255, 0.8);
}

[data-testid="stCameraInputSwitchButton"] {
  display: none !important;
}

/* RESPONSIVE KHUSUS MOBILE (MAX WIDTH 768px) */
@media (max-width: 768px) {
  .st-emotion-cache-z5fcl4 {
      flex-direction: column;
  }

  .header-box {
      font-size: 18px;
  }
  .mood-box-content h2 {
      font-size: 30px;
  }
  .mood-box-content {
      font-size: 16px;
  }
  .portrait-box p {
      font-size: 18px !important;
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

  div[data-testid="stCameraInput"] button {
      width: 120px;
      font-size: 14px;
      bottom: 10px;
      right: 50%;
      transform: translateX(50%);
  }

  .column-wrapper {
      flex-direction: row;
      height: auto;
      align-items: center;
      justify-content: space-around;
      margin-bottom: 20px;
  }

  .35thn-box, .mascot-box {
      width: 100px;
      height: auto;
      margin: 0;
  }

  img[src*="bakrieland_logo"] {
      height: 50px !important;
  }
  img[src*="google_logo"], img[src*="metrodata_logo"] {
      height: 30px !important;
  }

  div[data-testid="stHorizontalBlock"] {
      flex-direction: column;
  }

  /* Layout khusus HP: posisi ulang header, maskot, powered by */
  .st-emotion-cache-z5fcl4 > div:first-child > div {
    display: flex;
    flex-direction: column;
    align-items: center;
    position: relative;
    gap: 6px;
  }

  .column-wrapper {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    position: relative;
    width: 100%;
    padding: 0 12px;
  }

  .35thn-box {
    position: absolute;
    top: 0;
    left: 0;
    width: 70px;
  }

  .mascot-box {
    position: absolute;
    top: 140px;
    left: 0;
    width: 80px;
  }

  .mascot-box img {
    width: 100%;
    height: auto;
  }

  .st-emotion-cache-z5fcl4 > div:first-child > div:nth-child(3) > div {
    position: absolute;
    top: 0;
    right: 0;
    width: auto;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    padding-right: 12px;
  }

  .st-emotion-cache-z5fcl4 > div:first-child > div:nth-child(3) img {
    margin-bottom: 4px;
  }

  .st-emotion-cache-z5fcl4 > div:first-child > div:nth-child(3) span {
    font-size: 12px;
    color: #fff;
    text-align: right;
  }

  .camera-wrapper {
    margin-top: 90px;
  }
}
</style>
""", unsafe_allow_html=True)


# --- LOGIC & LAYOUT (TIDAK ADA PERUBAHAN DI SINI) ---
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
      st.write("")
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
        st.markdown('<div class="camera-wrapper"><div class="camera-frame"></div>', unsafe_allow_html=True)

        user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")
        st.markdown('</div>', unsafe_allow_html=True)

        if user_input is not None and user_input != st.session_state.last_photo:
            st.session_state.last_photo = user_input

            with st.spinner("Menganalisis suasana hati Anda..."):
                try:
                    image = Image.open(io.BytesIO(user_input.getvalue()))

                    prompt_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt.txt"
                    prompt_response = requests.get(prompt_url)
                    prompt_response.raise_for_status()
                    analysis_prompt = prompt_response.text

                    json_prompt_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt_json.txt"
                    json_prompt_response = requests.get(json_prompt_url)
                    json_prompt_response.raise_for_status()
                    json_prompt = json_prompt_response.text

                    analysis_response = model.generate_content([analysis_prompt, image])
                    raw_output = analysis_response.text

                    json_response = model.generate_content([json_prompt, raw_output])

                    filenames = json_response.text.strip().split(",")
                    if len(filenames) >= 4:
                        midpoint = len(filenames) // 2
                        first_filenames = filenames[:midpoint]
                        second_filenames = filenames[midpoint:]

                        first_target_names = [
                            "Bogor Nirwana Residence", "Kahuripan Nirwana", "Sayana Bogor",
                            "Taman Rasuna Epicentrum", "The Masterpiece & The Empyreal"
                        ]
                        first_filenames_edited = [
                            name.strip() + " " + str(random.randint(1, 2)) if name.strip() in first_target_names else name.strip()
                            for name in first_filenames
                        ]

                        second_target_names = [
                            "Aston Bogor", "Bagus Beach Walk", "Grand ELTY Krakatoa", "Hotel Aston Sidoarjo",
                            "Jungleland", "Junglesea Kalianda", "Rivera", "Swiss Belresidences Rasuna Epicentrum",
                            "The Alana Malioboro", "The Grove Suites", "The Jungle Waterpark"
                        ]
                        second_filenames_edited = [
                            name.strip() + " " + str(random.randint(1, 2)) if name.strip() in second_target_names else name.strip()
                            for name in second_filenames
                        ]

                        st.session_state.image_urls = [
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{first_filenames_edited[0].strip()}.jpg",
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{first_filenames_edited[1].strip()}.jpg",
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{second_filenames_edited[0].strip()}.jpg",
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{second_filenames_edited[1].strip()}.jpg"
                        ]
                        st.session_state.image_captions = [
                            first_filenames[0].strip(), first_filenames[1].strip(),
                            second_filenames[0].strip(), second_filenames[1].strip()
                        ]
                        st.session_state.analysis_result = raw_output
                    else:
                        st.session_state.analysis_result = "Gagal memproses rekomendasi gambar. Silakan coba lagi."

                except requests.exceptions.RequestException as http_err:
                    st.error(f"Gagal mengambil prompt: {http_err}")
                    st.session_state.analysis_result = "Terjadi kesalahan jaringan. Tidak dapat memuat model."
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat pemrosesan: {e}")
                    st.session_state.analysis_result = "Gagal menganalisis gambar. Silakan coba lagi."

            st.rerun()

        elif user_input is None and st.session_state.last_photo is not None:
            st.session_state.analysis_result = placeholder_analysis
            st.session_state.image_urls = [placeholder_url] * 4
            st.session_state.image_captions = [placeholder_caption] * 4
            st.session_state.last_photo = None
            st.rerun()
    with colA3:
      colA3row11 = st.container()
      with colA3row11:
        st.markdown("""
        <div>
          <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png" style="height: 70px; margin-bottom: 4px;" />
        </div>
        """, unsafe_allow_html=True)
      colA3row12 = st.container()
      with colA3row12:
        st.markdown("""
        <div>
          <span style="display: inline-block; vertical-align: middle;"><div>POWERED BY:</div></span>
        </div>
        """, unsafe_allow_html=True)
      colA3row13 = st.container()
      with colA3row13:
        st.markdown("""
        <div>
          <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png" style="height: 40px; vertical-align: middle; margin-left: -10px; margin-right: -30px;" />
          <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png" style="height: 40px; vertical-align: middle;" />
        </div>
        """, unsafe_allow_html=True)

row2 = st.container()
with row2:
    escaped_analysis = html.escape(st.session_state.analysis_result)
    st.markdown(f"""
    <div class="mood-box-content">
      <h2>Mood Analytic</h2>
      <pre style="white-space: pre-wrap; font-family: inherit;">{escaped_analysis}</pre>
    </div>
    """, unsafe_allow_html=True)

row3 = st.container()
with row3:
    colC1, colC2 = st.columns(2)
    with colC1:
        st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="portrait-box">
          <img src="{st.session_state.image_urls[0]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
          <p style="text-align:center; margin-top: 5px; font-size: 30px; color: #ccc;">{st.session_state.image_captions[0]}</p>
          <img src="{st.session_state.image_urls[1]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
          <p style="text-align:center; margin-top: 5px; font-size: 30px; color: #ccc;">{st.session_state.image_captions[1]}</p>
        </div>
        """, unsafe_allow_html=True)
    with colC2:
        st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="portrait-box">
          <img src="{st.session_state.image_urls[2]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
          <p style="text-align:center; margin-top: 5px; font-size: 30px; color: #ccc;">{st.session_state.image_captions[2]}</p>
          <img src="{st.session_state.image_urls[3]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
          <p style="text-align:center; margin-top: 5px; font-size: 30px; color: #ccc;">{st.session_state.image_captions[3]}</p>
        </div>
        """, unsafe_allow_html=True)

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