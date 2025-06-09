import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html

# Konfigurasi Halaman
st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# --- CSS Styling ---
# Menambahkan style untuk background, waves, dan custom boxes
st.markdown("""
<style>
/* Background Gradient Animation */
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

/* Animated Waves */
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

/* Custom Component Styling */
.stApp, [data-testid="stAppViewContainer"] {
  background: transparent !important;
  overflow: hidden !important;
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
    font-size: 10px;
    margin-top: 10px;
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
.mood-box-content ul {
    margin-top: 0;
    margin-bottom: 1em;
    padding-left: 20px;
}

/* --- MODIFIED: Circular Camera Input --- */
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

/* --- NEW: Camera Button Styling --- */

/* Style the "Take Photo" button (the one over the video) to be an icon */
div[data-testid="stCameraInput"] button:not(:has(span)) { /* Target button without span (Take Photo) */
    font-size: 0 !important; /* Hide original text */
    width: 60px !important;
    height: 60px !important;
    border-radius: 50% !important;
    background-color: rgba(255, 255, 255, 0.3) !important;
    border: 2px solid white !important;
    display: flex;
    align-items: center;
    justify-content: center;
    position: absolute;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
}

div[data-testid="stCameraInput"] button:not(:has(span))::after {
    content: '�'; /* Camera emoji icon */
    font-size: 28px;
    color: white;
    line-height: 1;
}

/* Style the "Clear photo" button to be smaller */
div[data-testid="stCameraInput"] button:has(span) { /* Target button with span (Clear photo) */
    background-color: rgba(0, 0, 0, 0.5) !important;
    border: 1px solid #00f0ff !important;
    color: #00f0ff !important;
    padding: 4px 12px !important; /* Smaller padding */
    width: auto !important; /* Auto width */
    min-height: auto !important;
    line-height: 1.5 !important;
    border-radius: 8px !important;
    margin-top: 10px;
}

div[data-testid="stCameraInput"] button:has(span):hover {
    box-shadow: 0 0 8px #00f0ff !important;
    background-color: rgba(0, 240, 255, 0.2) !important;
}

</style>
""", unsafe_allow_html=True)
# Add waves to the background
st.markdown('<div class="wave"></div><div class="wave"></div><div class="wave"></div>', unsafe_allow_html=True)


# --- Backend and Model Setup ---
try:
    genai.configure(api_key=st.secrets["gemini_api"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Error configuring Generative AI: {e}")
    st.stop()


# --- Main Layout ---
col_header_left, col_header_right = st.columns([0.85, 0.15])

with col_header_right:
    # Company Logos and Lottie Animation
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

    # --- State Management Initialization ---
    placeholder_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"
    placeholder_caption = ""
    placeholder_analysis = "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati dan mendapatkan rekomendasi yang dipersonalisasi."

    # Initialize session state if it doesn't exist
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = placeholder_analysis
        st.session_state.image_urls = [placeholder_url] * 4
        st.session_state.image_captions = [placeholder_caption] * 4
        st.session_state.last_photo = None
    
    # --- Recommendation Columns ---
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

    # --- Camera and Analysis Column ---
    with col3:
        user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")
        
        # --- REVISED LOGIC ---
        # This block executes if a new photo is taken.
        if user_input is not None and user_input != st.session_state.last_photo:
            st.session_state.last_photo = user_input
            
            with st.spinner("Menganalisis suasana hati Anda..."):
                try:
                    image = Image.open(io.BytesIO(user_input.getvalue()))

                    # Fetch prompts from GitHub
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

                        # Update state with new results
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

        # This block executes if the user clicks "Clear photo"
        elif user_input is None and st.session_state.last_photo is not None:
            # Reset to placeholders
            st.session_state.analysis_result = placeholder_analysis
            st.session_state.image_urls = [placeholder_url] * 4
            st.session_state.image_captions = [placeholder_caption] * 4
            st.session_state.last_photo = None
            st.rerun()
            
        # Display the analysis box with the current state
        escaped_analysis = html.escape(st.session_state.analysis_result)
        st.markdown(f"""
        <div class="mood-box-content">
            <pre style="white-space: pre-wrap; font-family: inherit; font-size: 1.2em;">{escaped_analysis}</pre>
        </div>
        """, unsafe_allow_html=True)