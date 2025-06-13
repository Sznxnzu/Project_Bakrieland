import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html

st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], .stApp {
    background: none !important;
    background-image: url("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/wallpaper/wallpaper_2.png") !important;
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
    font-size: 18px;
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
.mood-box-content {
    border: 2px solid #00f0ff;
    background-color: rgba(10, 15, 30, 0.85);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 20px #00f0ff;
    font-size: 15px;
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

div[data-testid="stCameraInput"] {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
}

div[data-testid="stCameraInput"] > div{
    width: 300px !important;
    height: 300px !important;
    border-radius: 50% !important;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(0,240,255,0.5);
    position: relative;
}


div[data-testid="stCameraInput"] video,
div[data-testid="stCameraInput"] img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 50%;
}

div[data-testid="stCameraInput"] button {
    all: unset;
    padding: 8px 16px;
    background-color: #00f0ff;
    color: black;
    font-weight: bold;
    border-radius: 6px;
    cursor: pointer;
    text-align: center;
    margin-top: 8px;
    box-shadow: 0 0 10px rgba(0,240,255,0.7);
}
div[data-testid="stCameraInput"] button:hover {
    background-color: #00c0cc;
}


</style>
""", unsafe_allow_html=True)

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
    with colA2:
        user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")

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

                        st.session_state.image_urls = [
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{first_filenames[0].strip()}.jpg",
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{first_filenames[1].strip()}.jpg",
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{second_filenames[0].strip()}.jpg",
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{second_filenames[1].strip()}.jpg"
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
          <p style="text-align:center; margin-top: 5px; font-size: 0.9em; color: #ccc;">{st.session_state.image_captions[0]}</p>
          <img src="{st.session_state.image_urls[1]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
          <p style="text-align:center; margin-top: 5px; font-size: 0.9em; color: #ccc;">{st.session_state.image_captions[1]}</p>
        </div>
        """, unsafe_allow_html=True)
    with colC2:
        st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="portrait-box">
          <img src="{st.session_state.image_urls[2]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
          <p style="text-align:center; margin-top: 5px; font-size: 0.9em; color: #ccc;">{st.session_state.image_captions[2]}</p>
          <img src="{st.session_state.image_urls[3]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
          <p style="text-align:center; margin-top: 5px; font-size: 0.9em; color: #ccc;">{st.session_state.image_captions[3]}</p>
        </div>
        """, unsafe_allow_html=True)
