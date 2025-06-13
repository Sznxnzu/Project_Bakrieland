import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import cv2
import numpy as np
from PIL import Image
import requests
import io
import html
import google.generativeai as genai

# --- Streamlit UI Config ---
st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")
st.markdown("""
<style>
.stApp {
  background-image: url("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/wallpaper/wallpaper_2.png");
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
}
::-webkit-scrollbar {
  display: none;
}
</style>
""", unsafe_allow_html=True)

# --- Gemini Setup ---
try:
    genai.configure(api_key=st.secrets["gemini_api"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Error configuring Generative AI: {e}")
    st.stop()

# --- Defaults ---
placeholder_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"
placeholder_analysis = "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati."

# --- Session State ---
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = placeholder_analysis
    st.session_state.image_urls = [placeholder_url] * 4
    st.session_state.image_captions = [""] * 4
    st.session_state.last_photo = None
    st.session_state["captured_frame"] = None

# --- Video Processor ---
class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.frame = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.frame = img.copy()
        return img

# --- Streamlit WebRTC Camera ---
ctx = webrtc_streamer(
    key="camera",
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

# --- Photo Capture Button ---
if st.button("📸 Ambil Foto"):
    if ctx.video_processor and ctx.video_processor.frame is not None:
        st.session_state["captured_frame"] = ctx.video_processor.frame.copy()
        st.rerun()

# --- Process Captured Frame ---
user_input = st.session_state["captured_frame"]
if user_input is not None and not np.array_equal(user_input, st.session_state.last_photo):
    st.session_state.last_photo = user_input
    image_pil = Image.fromarray(cv2.cvtColor(user_input, cv2.COLOR_BGR2RGB))
    st.image(image_pil, caption="Captured Face", use_column_width=True)

    # --- Analysis ---
    with st.spinner("Menganalisis suasana hati Anda..."):
        try:
            # Load prompts
            prompt_response = requests.get("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt.txt")
            prompt_response.raise_for_status()
            analysis_prompt = prompt_response.text

            json_prompt_response = requests.get("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt_json.txt")
            json_prompt_response.raise_for_status()
            json_prompt = json_prompt_response.text

            # Gemini image analysis
            analysis_response = model.generate_content([analysis_prompt, image_pil])
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
                st.session_state.image_captions = [f.strip() for f in filenames]
                st.session_state.analysis_result = raw_output
            else:
                st.session_state.analysis_result = "Gagal memproses rekomendasi gambar."

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
            st.session_state.analysis_result = "Gagal menganalisis gambar."

# --- Display Result ---
escaped_analysis = html.escape(st.session_state.analysis_result)
st.markdown(f"""
<div class="mood-box-content">
  <pre style="white-space: pre-wrap; font-family: inherit; font-size: 1.2em;">{escaped_analysis}</pre>
</div>
""", unsafe_allow_html=True)

# --- Recommendations Display ---
colC1, colC2 = st.columns(2)
with colC1:
    st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
    for i in range(2):
        st.image(st.session_state.image_urls[i], caption=st.session_state.image_captions[i], use_column_width=True)
with colC2:
    st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
    for i in range(2, 4):
        st.image(st.session_state.image_urls[i], caption=st.session_state.image_captions[i], use_column_width=True)
