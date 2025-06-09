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
/* Circular camera styling */
div[data-testid="stCameraInput"] {
    display: flex;
    flex-direction: column;
    align-items: center;
}
div[data-testid="stCameraInput"] > div {
    border-radius: 50% !important;
    width: 270px !important;
    height: 270px !important;
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
.button-row {
    display: flex;
    justify-content: center;
    gap: 18px;
    margin-top: 10px;
    margin-bottom: 10px;
}
.stButton > button.icon-btn {
    background: #181c2b;
    border: none;
    border-radius: 50%;
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 12px #00f0ff33;
    font-size: 22px;
    cursor: pointer;
    transition: box-shadow .15s;
}
.stButton > button.icon-btn:hover { box-shadow: 0 0 24px #00f0ff88; background: #222; }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
placeholder_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"
placeholder_caption = ""
placeholder_analysis = "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati dan mendapatkan rekomendasi yang dipersonalisasi."
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = placeholder_analysis
    st.session_state.image_urls = [placeholder_url] * 4
    st.session_state.image_captions = [placeholder_caption] * 4
    st.session_state.last_photo = None
    st.session_state.photo_to_analyze = None

col1, col2, col3 = st.columns([1, 1, 1.4])
with col3:
    user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")
    
    # Tombol horizontal
    colp, colr = st.columns(2)
    with colp:
        # Tombol proses foto (ikon kamera)
        if st.button("📸", key="process_photo", help="Proses Foto", use_container_width=True):
            if user_input is not None:
                st.session_state.photo_to_analyze = user_input
    with colr:
        # Tombol reset/clear
        if st.button("🔄", key="reset_photo", help="Clear Photo", use_container_width=True):
            st.session_state.photo_to_analyze = None
            st.session_state.last_photo = None
            st.session_state.analysis_result = placeholder_analysis
            st.session_state.image_urls = [placeholder_url] * 4
            st.session_state.image_captions = [placeholder_caption] * 4
            st.experimental_rerun()

    # Proses foto jika ada
    if st.session_state.photo_to_analyze is not None and st.session_state.last_photo != st.session_state.photo_to_analyze:
        st.session_state.last_photo = st.session_state.photo_to_analyze
        try:
            genai.configure(api_key=st.secrets["gemini_api"])
            model = genai.GenerativeModel("models/gemini-2.5-flash-preview-04-17-thinking")
            with st.spinner("Menganalisis suasana hati Anda..."):
                image = Image.open(io.BytesIO(st.session_state.photo_to_analyze.getvalue()))
                prompt_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt.txt"
                analysis_prompt = requests.get(prompt_url).text
                json_prompt_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt_json.txt"
                json_prompt = requests.get(json_prompt_url).text
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
        except Exception as e:
            st.error(f"Terjadi kesalahan saat pemrosesan: {e}")
            st.session_state.analysis_result = "Gagal menganalisis gambar. Silakan coba lagi."
        st.experimental_rerun()

    # Tampilkan hasil analisis (box)
    escaped_analysis = html.escape(st.session_state.analysis_result)
    st.markdown(f"""
    <div class="mood-box-content">
        <pre style="white-space: pre-wrap; font-family: inherit; font-size: 1.2em;">{escaped_analysis}</pre>
    </div>
    """, unsafe_allow_html=True)
