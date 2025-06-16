import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import random
import qrcode # Import library qrcode
import base64 # Import base64 untuk menampilkan gambar QR

st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# --- CSS Styling ---
st.markdown("""
<style>
/* Background and Scrollbar */
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

/* Header Box */
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
/* Portrait Box for Recommendations */
.portrait-box {
    border: 2px solid #00f0ff;
    background-color: rgba(0,0,30,0.6);
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px #00f0ff;
    text-align: center;
}

/* Column Wrapper for Side Elements */
.column-wrapper {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 400px; /* Adjust based on your layout */
}

/* 35th Anniversary Logo Box */
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

/* Mascot Box */
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

/* Mood Analysis Content Box */
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
    /* --- NEW: Add a specific ID for screenshot targeting --- */
    position: relative; /* Needed if you want absolutely positioned children, etc. */
}
.mood-box-content:hover {
    box-shadow: 0 0 25px #00f0ff, 0 0 50px #00f0ff;
}
.mood-box-content p {
    margin-bottom: 0;
}
.mood-box-content h2{
    font-size: 45px;
    color: #fff; /* Ensure heading color is visible */
    text-align: center;
    margin-top: 0;
    margin-bottom: 15px;
}
.mood-box-content pre { /* Style for the pre tag inside mood-box-content */
    color: #fff;
    font-size: 1.2em; /* Increase font size for readability in screenshot */
}
.mood-box-content ul {
    margin-top: 0;
    margin-bottom: 1em;
    padding-left: 20px;
}

/* Camera Input Styles */
div[data-testid="stCameraInput"] div {
    background-color: transparent !important;
}
div[data-testid="stCameraInputWebcamStyledBox"] {
    width: 500px !important;
    height: 500px !important;
    border-radius: 50% !important;
    overflow: hidden;
    margin: auto;
    box-shadow: 0 0 20px rgba(0,240,255,0.5);
}
div[data-testid="stCameraInput"] video{
    object-fit: cover;
    width: 100%;
    height: 100%;
    border-radius: 0;
}
div[data-testid="stCameraInput"] img {
    display: block;
    object-fit: cover;
    width: 300px !important; /* Adjusted for better fit in circular frame */
    height: 300px !important; /* Adjusted for better fit in circular frame */
    border-radius: 50% !important;
    box-shadow: 0 0 20px rgba(0,240,255,0.5);
    margin: auto;
}
div[data-testid="stCameraInput"] button {
    margin-top: 12px;
    z-index: 10;
    position: relative;
    padding: 10px 20px;
    background-color: #00c0cc;
    color: #000;
    font-weight: 600;
    font-size: 16px;
    border: none;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 240, 255, 0.6);
    cursor: pointer;
    transition: all 0.2s ease-in-out;
}
div[data-testid="stCameraInput"] button:hover {
    background-color: #00aabb;
    transform: scale(1.05);
    box-shadow: 0 6px 16px rgba(0, 240, 255, 0.8);
}

/* QR Code Styling */
.qr-box {
    border: 2px solid #00f0ff;
    background-color: rgba(0,0,30,0.6);
    border-radius: 8px;
    padding: 10px;
    margin-top: 20px;
    box-shadow: 0 0 10px #00f0ff;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.qr-box img {
    width: 150px; /* Fixed size for QR code image */
    height: 150px;
    object-fit: contain;
    margin-bottom: 10px;
}
.qr-box p {
    color: #00f0ff;
    font-size: 0.9em;
    margin: 0;
}
/* Style for Download button */
.stDownloadButton button {
    display: block;
    margin: 20px auto; /* Center the button below the mood box */
    padding: 12px 25px;
    background-color: #00c0cc;
    color: #000;
    font-weight: 600;
    font-size: 18px;
    border: none;
    border-radius: 8px;
    box-shadow: 0 6px 15px rgba(0, 240, 255, 0.7);
    cursor: pointer;
    transition: all 0.2s ease-in-out;
}
.stDownloadButton button:hover {
    background-color: #00aabb;
    transform: scale(1.03);
    box-shadow: 0 8px 20px rgba(0, 240, 255, 0.9);
}
</style>
""", unsafe_allow_html=True)


# --- Backend and Model Setup ---
try:
    genai.configure(api_key=st.secrets["gemini_api"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Error configuring Generative AI: {e}")
    st.stop()

# --- Fungsi untuk membuat QR Code ---
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

# --- State Management Initialization ---
placeholder_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"
placeholder_caption = ""
placeholder_analysis = "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati dan mendapatkan rekomendasi yang dipersonalisasi."

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = placeholder_analysis
    st.session_state.image_urls = [placeholder_url] * 4
    st.session_state.image_captions = [placeholder_caption] * 4
    st.session_state.last_photo = None

# --- Main Layout ---
row1 = st.container()
with row1:
    colA1, colA2, colA3 = st.columns([0.2, 0.6, 0.2])
    with colA1:
        st.write("") # Placeholder for top-left content
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

                        first_target_names = [
                            "Bogor Nirwana Residence", "Kahuripan Nirwana", "Sayana Bogor",
                            "Taman Rasuna Epicentrum", "The Masterpiece & The Empyreal"
                        ]

                        first_filenames_edited = [
                            name.strip() + " " + str(random.randint(1, 2)) if name.strip() in first_target_names else name.strip()
                            for name in first_filenames
                        ]

                        second_target_names = [
                            "Aston Bogor", "Bagus Beach Walk", "Grand ELTY Krakatoa",
                            "Hotel Aston Sidoarjo", "Jungleland", "Junglesea Kalianda",
                            "Rivera", "Swiss Belresidences Rasuna Epicentrum",
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
        # Company Logos
        st.markdown("""
        <div>
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png" style="height: 70px; margin-bottom: 4px;" />
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div>
            <span style="display: inline-block; vertical-align: middle;"><div>POWERED BY:</div></span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div>
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png" style="height: 40px; vertical-align: middle; margin-left: -10px; margin-right: -30px;" />
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png" style="height: 40px; vertical-align: middle;" />
        </div>
        """, unsafe_allow_html=True)

        # --- QR Code Section (NEW LOCATION) ---
        # Mendapatkan URL aplikasi Streamlit saat ini
        # Penting: Ganti placeholder ini dengan URL aplikasi Anda yang sebenarnya saat di-deploy!
        # Misalnya: current_app_url = "https://your-streamlit-app-name.streamlit.app"
        current_app_url = "https://example.com/your-bakrieland-app" # <<< GANTI INI DENGAN URL ASLI APPLIKASI ANDA

        # Buat QR code dari URL aplikasi
        qr_image_bytes = generate_qr_code(current_app_url)

        st.markdown(f"""
            <div class="qr-box">
                <img src="data:image/png;base64,{base64.b64encode(qr_image_bytes).decode('utf-8')}" alt="QR Code" />
                <p>Scan untuk kembali ke halaman utama.</p>
            </div>
        """, unsafe_allow_html=True)


row2 = st.container()
with row2:
    # --- Tambahkan ID ke elemen mood-box-content untuk screenshot ---
    escaped_analysis = html.escape(st.session_state.analysis_result)
    st.markdown(f"""
    <div id="mood-analysis-section" class="mood-box-content">
        <h2>Mood Analytic</h2>
        <pre style="white-space: pre-wrap; font-family: inherit;">{escaped_analysis}</pre>
    </div>
    """, unsafe_allow_html=True)

    # --- Tombol untuk mengunduh hasil analisis (NEW) ---
    if st.button("Unduh Hasil Analisis", key="download_analysis_button"):
        # HTML dan JavaScript untuk mengambil screenshot dan mengunduh
        components.html(
            f"""
            <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
            <script>
                function downloadMoodAnalysis() {{
                    const element = document.getElementById('mood-analysis-section');
                    // Tambahkan elemen lain yang ingin di-screenshot jika perlu, misalnya gabungkan mood-box dan rekomendasi
                    // const fullPageElement = document.body; // atau specific container div jika ada

                    html2canvas(element, {{ 
                        scale: 2, // Meningkatkan resolusi gambar untuk kualitas lebih baik
                        backgroundColor: 'rgba(10, 15, 30, 0.85)', // Sesuaikan dengan warna latar belakang mood-box-content
                        useCORS: true, // Penting jika ada gambar eksternal (misal: dari GitHub)
                        logging: false // Matikan logging konsol html2canvas
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
            height=0, # Atur tinggi ke 0 agar tidak terlihat di UI
            width=0,
        )


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