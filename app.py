import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html

st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# CSS styling
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
  margin: 0;
  padding: 0;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, sans-serif;
  background: linear-gradient(315deg, rgba(101,0,94,1) 3%, rgba(60,132,206,1) 38%, rgba(48,238,226,1) 68%, rgba(255,25,25,1) 98%);
  animation: gradient 15s ease infinite;
  background-size: 400% 400%;
  background-attachment: fixed;
}
@keyframes gradient {
  0% { background-position: 0% 0%; }
  50% { background-position: 100% 100%; }
  100% { background-position: 0% 0%; }
}
.wave {
  background: rgb(255 255 255 / 25%);
  border-radius: 1000% 1000% 0 0;
  position: fixed;
  width: 200%;
  height: 12em;
  animation: wave 10s -3s linear infinite;
  transform: translate3d(0, 0, 0);
  opacity: 0.8;
  bottom: 0;
  left: 0;
  z-index: -1;
}
.wave:nth-of-type(2) {
  bottom: -1.25em;
  animation: wave 18s linear reverse infinite;
  opacity: 0.8;
}
.wave:nth-of-type(3) {
  bottom: -2.5em;
  animation: wave 20s -1s reverse infinite;
  opacity: 0.9;
}
@keyframes wave {
  2%   { transform: translateX(1); }
  25%  { transform: translateX(-25%); }
  50%  { transform: translateX(-50%); }
  75%  { transform: translateX(-25%); }
  100% { transform: translateX(1); }
}
/* Custom circular camera styling */
div[data-testid="stCameraInput"] {
    display: flex;
    flex-direction: column;
    align-items: center;
}
div[data-testid="stCameraInput"] > div {
    border-radius: 50% !important;
    width: 250px !important;
    height: 250px !important;
    margin: 0 auto !important;
    overflow: hidden;
    box-shadow: 0 0 20px rgba(0,240,255,0.5);
    transition: transform 0.3s ease;
    background: #222;
}
div[data-testid="stCameraInput"] > div:hover {
    transform: scale(1.02);
}
div[data-testid="stCameraInput"] video,
div[data-testid="stCameraInput"] img {
    object-fit: cover;
    width: 100%;
    height: 100%;
    border-radius: 0;
}
/* Tombol horizontal */
.button-row {
    display: flex;
    justify-content: center;
    gap: 18px;
    margin-top: 16px;
    margin-bottom: 12px;
}
.icon-btn {
    background: #181c2b;
    border: none;
    border-radius: 50%;
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 12px #00f0ff33;
    font-size: 22px;
    cursor: pointer;
    transition: box-shadow .15s;
    margin: 0 2px;
}
.icon-btn:hover { box-shadow: 0 0 24px #00f0ff88; background: #222; }
</style>
<div class="wave"></div><div class="wave"></div><div class="wave"></div>
""", unsafe_allow_html=True)

# Initial placeholders
placeholder_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"
placeholder_caption = ""
placeholder_analysis = "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati dan mendapatkan rekomendasi yang dipersonalisasi."

# Session state init
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = placeholder_analysis
    st.session_state.image_urls = [placeholder_url] * 4
    st.session_state.image_captions = [placeholder_caption] * 4
    st.session_state.last_photo = None
    st.session_state.ready_to_analyze = False

# Header & Layout
col_header_left, col_header_right = st.columns([0.85, 0.15])
with col_header_right:
    st.markdown("""
    <div style="position: absolute; top: -30px; right: -70px;">
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png" style="height: 70px; margin-bottom: 4px;" />
        <div style="font-size: 11px; color: #ccc;">
            <span style="display: inline-block; vertical-align: middle;">POWERED BY:</span>
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png" style="height: 40px; vertical-align: middle; margin-left: -10px; margin-right: -30px;" />
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png" style="height: 40px; vertical-align: middle;" />
        </div>
    </div>
    """, unsafe_allow_html=True)
    components.html("""
    <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    <div style="display: flex; justify-content: center; align-items: center;">
        <lottie-player 
            id="robot"
            src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/Animation%20-%201749118794076.json"
            background="transparent" speed="1" style="width: 300px; height: 300px;"
            autoplay loop>
        </lottie-player>
    </div>
    <script>
        document.getElementById("robot").addEventListener("click", function() {
            const r = document.getElementById("robot");
            r.stop();
            r.play();
        });
    </script>
    """, height=340)
    st.markdown("""
        <div class="qr-box">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/qr_logo.png" style="width:100%; border-radius: 8px;" />
        </div>
    """, unsafe_allow_html=True)

with col_header_left:
    col1, col2, col3 = st.columns([1, 1, 1.4])
    with col1:
        st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="portrait-box">
            <img src="{st.session_state.image_urls[0]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
            <p style="text-align:center; margin-top: 5px; font-size: 0.9em; color: #ccc;">{st.session_state.image_captions[0]}</p>
            <img src="{st.session_state.image_urls[1]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
            <p style="text-align:center; margin-top: 5px; font-size: 0.9em; color: #ccc;">{st.session_state.image_captions[1]}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="portrait-box">
            <img src="{st.session_state.image_urls[2]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
            <p style="text-align:center; margin-top: 5px; font-size: 0.9em; color: #ccc;">{st.session_state.image_captions[2]}</p>
            <img src="{st.session_state.image_urls[3]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
            <p style="text-align:center; margin-top: 5px; font-size: 0.9em; color: #ccc;">{st.session_state.image_captions[3]}</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        # Kamera lingkaran
        user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")
        # Tampilkan tombol proses (kamera) & clear photo (refresh) horizontal
        st.markdown(
            """
            <div class="button-row">
                <form method="post">
                    <button class="icon-btn" name="process" type="submit" style="margin-right:2px;" title="Process Photo">&#128247;</button>
                    <button class="icon-btn" name="clear" type="submit" style="margin-left:2px;" title="Clear Photo">&#x21bb;</button>
                </form>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Button logic (dengan workaround)
        # Gunakan query_params agar event tetap stateful walau pakai HTML form
        query_params = st.experimental_get_query_params()
        process_clicked = "process" in query_params
        clear_clicked = "clear" in query_params

        # Logic tombol process photo
        if process_clicked and user_input is not None:
            st.experimental_set_query_params()  # reset param supaya ga repeat
            try:
                genai.configure(api_key=st.secrets["gemini_api"])
                model = genai.GenerativeModel("models/gemini-2.5-flash-preview-04-17-thinking")
            except Exception as e:
                st.error(f"Error configuring Generative AI: {e}")
                st.stop()
            with st.spinner("Menganalisis suasana hati Anda..."):
                try:
                    image = Image.open(io.BytesIO(user_input.getvalue()))
                    # Fetch prompt
                    prompt_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt.txt"
                    prompt_response = requests.get(prompt_url)
                    prompt_response.raise_for_status()
                    analysis_prompt = prompt_response.text
                    json_prompt_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt_json.txt"
                    json_prompt_response = requests.get(json_prompt_url)
                    json_prompt_response.raise_for_status()
                    json_prompt = json_prompt_response.text
                    # Generate mood analysis
                    analysis_response = model.generate_content([analysis_prompt, image])
                    raw_output = analysis_response.text
                    # Generate JSON for image filenames
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
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat pemrosesan: {e}")
                    st.session_state.analysis_result = "Gagal menganalisis gambar. Silakan coba lagi."
            st.experimental_rerun()

        # Logic tombol clear photo
        elif clear_clicked:
            st.experimental_set_query_params()
            st.session_state.analysis_result = placeholder_analysis
            st.session_state.image_urls = [placeholder_url] * 4
            st.session_state.image_captions = [placeholder_caption] * 4
            st.session_state.last_photo = None
            st.experimental_rerun()

        # Tampilkan hasil analisis (box)
        escaped_analysis = html.escape(st.session_state.analysis_result)
        st.markdown(f"""
        <div class="mood-box-content">
            <pre style="white-space: pre-wrap; font-family: inherit; font-size: 1.2em;">{escaped_analysis}</pre>
        </div>
        """, unsafe_allow_html=True)
