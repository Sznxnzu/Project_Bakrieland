import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import qrcode # Import library qrcode untuk membuat QR Code

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
    /* Memberikan ID agar mudah ditangkap oleh JavaScript */
    position: relative; /* Penting untuk positioning QR jika mau diletakkan di sini */
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
/* Center the entire camera input block */
div[data-testid="stCameraInput"] {
    display: flex;
    flex-direction: column;
    align-items: center;
}
/* Style the main container for the video feed */
div[data-testid="stCameraInput"] > div {
    border-radius: 50% !important; /* Make it a circle */
    width: 250px !important;       /* Force width */
    height: 250px !important;       /* Force height */
    margin: 0 auto !important;      /* Center horizontally */
    overflow: hidden;               /* Hide the parts of the video outside the circle */
    box-shadow: 0 0 20px rgba(0,240,255,0.5);
    transition: transform 0.3s ease;
}
div[data-testid="stCameraInput"] > div:hover {
    transform: scale(1.02);
}
/* Ensure the video or image fills the circular frame without distortion */
div[data-testid="stCameraInput"] video,
div[data-testid="stCameraInput"] img {
    object-fit: cover;
    width: 100%;
    height: 100%;
    border-radius: 0; /* Remove any radius from the element itself */
}

/* Style for the QR Code Box */
.qr-box {
    border: 2px solid #00f0ff;
    background-color: rgba(0,0,30,0.6);
    border-radius: 8px;
    padding: 10px;
    margin-top: 20px; /* Adjust spacing as needed */
    box-shadow: 0 0 10px #00f0ff;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.qr-box img {
    width: 150px; /* Set a fixed size for the QR code image */
    height: 150px;
    object-fit: contain;
    margin-bottom: 10px;
}
.qr-box p {
    color: #00f0ff;
    font-size: 0.9em;
    margin: 0;
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

# Fungsi untuk membuat QR Code
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

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

    # --- QR Code Section ---
    # Mendapatkan URL aplikasi Streamlit saat ini
    # Di lingkungan lokal, ini mungkin 'http://localhost:8501'
    # Di lingkungan deploy, ini akan menjadi URL publik Streamlit Anda
    # Karena Streamlit tidak secara langsung menyediakan URL host, kita asumsikan base URL adalah '/'
    # Jika di deploy, Anda perlu tahu URL aplikasi Anda, misalnya dari st.experimental_get_query_params()
    # Untuk demo lokal, kita bisa menggunakan placeholder atau hardcode localhost
    
    # Untuk mendapatkan URL aplikasi Streamlit yang di-deploy, seringkali harus dari lingkungan.
    # Jika Anda menggunakan Streamlit Cloud, URL-nya akan terlihat seperti 'https://<nama_aplikasi>.<region>.streamlit.app/'
    # Untuk tujuan demo, saya akan menggunakan placeholder. Di produksi, ganti ini.
    # Misalnya, jika Anda tahu URL-nya: current_app_url = "https://your-app-name.streamlit.app"
    
    # Pendekatan umum untuk mendapatkan hostname di Streamlit (tidak selalu berhasil di semua deployment)
    # import socket
    # try:
    #     current_host = socket.gethostname()
    #     current_port = os.environ.get('PORT', '8501') # Default Streamlit port
    #     current_app_url = f"http://{current_host}:{current_port}"
    # except Exception:
    #     current_app_url = "http://localhost:8501" # Fallback for local testing

    # Alternatif sederhana untuk Streamlit Cloud atau Heroku deployment:
    # Anda bisa coba membaca environment variable yang disediakan oleh platform hosting Anda.
    # Contoh untuk Streamlit Cloud:
    # current_app_url = os.getenv("STREAMLIT_SERVER_URL", "http://localhost:8501") 
    # Atau jika Anda mengerti URL aplikasi Anda:
    current_app_url = "https://your-streamlit-app-url.com" # Ganti dengan URL aplikasi Anda yang sebenarnya!

    # Buat QR code dari URL aplikasi
    qr_image_bytes = generate_qr_code(current_app_url)

    st.markdown(f"""
        <div class="qr-box">
            <img src="data:image/png;base64,{base64.b64encode(qr_image_bytes).decode('utf-8')}" alt="QR Code" />
            <p>Scan untuk kembali ke halaman utama aplikasi.</p>
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
        # --- Penting: Beri ID unik ke elemen yang akan di-screenshot ---
        st.markdown(f"""
        <div id="mood-analysis-section" class="mood-box-content">
            <pre style="white-space: pre-wrap; font-family: inherit; font-size: 1.2em; color: #fff;">{html.escape(st.session_state.analysis_result)}</pre>
        </div>
        """, unsafe_allow_html=True)

        # Tombol untuk mengunduh hasil analisis
        if st.button("Unduh Hasil Analisis", key="download_button"):
            # HTML dan JavaScript untuk mengambil screenshot dan mengunduh
            components.html(
                f"""
                <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
                <script>
                    function downloadMoodAnalysis() {{
                        const element = document.getElementById('mood-analysis-section');
                        html2canvas(element, {{ 
                            scale: 2, // Meningkatkan resolusi gambar
                            backgroundColor: 'rgba(10, 15, 30, 0.85)', // Cocokkan dengan background mood-box-content
                            useCORS: true // Penting jika ada gambar dari domain lain
                        }}).then(canvas => {{
                            const link = document.createElement('a');
                            link.download = 'hasil_analisis_mood.png';
                            link.href = canvas.toDataURL('image/png');
                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                        }});
                    }}
                    // Panggil fungsi segera setelah tombol diklik
                    downloadMoodAnalysis();
                </script>
                """,
                height=0, # Atur tinggi ke 0 agar tidak memakan ruang visual
            )