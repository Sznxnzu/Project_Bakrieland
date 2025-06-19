import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import random

# Konfigurasi halaman tetap sama
st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# --- CSS STYLES (BAGIAN INI YANG DIMODIFIKASI) ---
# URL gambar layout dari Canva Anda untuk dijadikan latar belakang
CANVA_LAYOUT_URL = "https://i.ibb.co/6gq1v8p/image-604ba2.png"
# URL untuk overlay bingkai kamera (Anda perlu membuatnya dari Canva)
CAMERA_FRAME_URL = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/camera_frame_overlay.png" # Contoh URL, ganti dengan milik Anda

st.markdown(f"""
<style>
/* Gaya dasar menggunakan layout Canva sebagai background */
html, body, [data-testid="stAppViewContainer"], .stApp {{
    background-image: url('{CANVA_LAYOUT_URL}');
    background-color: #0A1942; /* Fallback color */
    background-size: cover;
    background-position: center top;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* Sembunyikan scrollbar */
::-webkit-scrollbar {{
  display: none;
}}

/* Wrapper untuk menempatkan semua konten agar sesuai dengan layout background */
.main-content-wrapper {{
    max-width: 540px; /* Sesuaikan lebar ini agar pas dengan layout di background */
    margin: 0 auto;
    padding-top: 10px; /* Jarak dari atas */
}}

/* ------------------------------------------------------------------------- */
/* STYLING BARU BERDASARKAN DESAIN CANVA */
/* ------------------------------------------------------------------------- */

/* Class untuk container utama dari setiap kotak (frame) */
.canva-frame-container {{
    padding: 10px;
    margin-bottom: 25px; /* Jarak antar frame */
    position: relative;
}}

/* Class untuk konten di dalam frame */
.canva-frame-content {{
    background-color: rgba(13, 36, 91, 0.85); /* Warna biru tua transparan */
    border: 1px solid #00D1FF;
    border-radius: 8px;
    padding: 20px;
    min-height: 150px;
    box-shadow: 0 0 15px rgba(0, 209, 255, 0.4);
    position: relative;
}}

/* Dekorasi sudut untuk frame (efek sci-fi) */
.canva-frame-content::before, .canva-frame-content::after {{
    content: '';
    position: absolute;
    width: 25px;
    height: 25px;
    border-color: #00D1FF;
    border-style: solid;
}}
.canva-frame-content::before {{
    top: -5px;
    left: -5px;
    border-width: 2px 0 0 2px;
    border-top-left-radius: 8px;
}}
.canva-frame-content::after {{
    bottom: -5px;
    right: -5px;
    border-width: 0 2px 2px 0;
    border-bottom-right-radius: 8px;
}}

/* Class untuk judul di dalam frame */
.canva-frame-title {{
    color: #FFFFFF;
    font-family: 'Orbitron', sans-serif;
    letter-spacing: 1px;
    text-align: center;
    font-size: 16px;
    margin-bottom: 15px;
    font-weight: bold;
    text-transform: uppercase;
}}


/* ------------------------------------------------------------------------- */
/* PENYESUAIAN LAYOUT UTAMA */
/* ------------------------------------------------------------------------- */
.logo-container {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 0 15px;
    margin-top: 20px;
}}

.logo-container img.logo-35thn {{
    width: 80px;
}}
.logo-container img.logo-bakrieland {{
    width: 100px;
}}

.powered-by-container {{
    text-align: right;
}}
.powered-by-container span {{
    color: white;
    font-size: 12px;
}}
.powered-by-container img {{
    height: 25px;
    margin-left: 5px;
}}

.mascot-container {{
    position: absolute;
    top: 130px;
    left: 20px;
    width: 90px;
}}

/* ------------------------------------------------------------------------- */
/* STYLING KAMERA DENGAN OVERLAY */
/* ------------------------------------------------------------------------- */
.camera-container {{
    position: relative;
    width: 280px;  /* Sesuaikan ukuran ini */
    height: 280px; /* Sesuaikan ukuran ini */
    margin: 30px auto 0 auto; /* Jarak dari atas */
}}

.camera-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('{CAMERA_FRAME_URL}');
    background-size: contain;
    background-repeat: no-repeat;
    pointer-events: none; /* Membuat overlay tidak bisa diklik */
    z-index: 10;
}}

div[data-testid="stCameraInput"] {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100% !important;
    height: 100% !important;
}}
div[data-testid="stCameraInput"] video,
div[data-testid="stCameraInput"] img,
div[data-testid="stCameraInputWebcamStyledBox"] {{
    border-radius: 50% !important;
    width: 100% !important;
    height: 100% !important;
    object-fit: cover;
}}
div[data-testid="stCameraInput"] button {{
    display: none; /* Sembunyikan tombol default */
}}
/* Tombol kamera custom jika diperlukan (saat ini disembunyikan) */
.custom-camera-button {{
    position: absolute;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 20;
}}

/* Penyesuaian untuk Rekomendasi Gambar */
.recommendation-box img {{
    width:100%;
    height:180px;
    border-radius:8px;
    object-fit:cover;
    margin-bottom: 10px;
}}
.recommendation-box p {{
    text-align:center;
    font-size: 18px;
    color: #ccc;
    font-weight: bold;
    margin-top: 5px;
    margin-bottom: 15px;
}}
.recommendation-box p:last-child {{
    margin-bottom: 0;
}}

/* Responsive untuk mobile */
@media (max-width: 768px) {{
    .main-content-wrapper {{ max-width: 95%; }}
    .camera-container {{ width: 220px; height: 220px; }}
    .mascot-container {{ display: none; }} /* Sembunyikan maskot di mobile agar tidak menumpuk */
}}

</style>
""", unsafe_allow_html=True)


# --- WRAPPER UNTUK KONTEN UTAMA ---
st.markdown('<div class="main-content-wrapper">', unsafe_allow_html=True)


# --- LOGIC & LAYOUT (Python-side) ---
try:
    genai.configure(api_key=st.secrets["gemini_api"])
    model = genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    st.error(f"Error configuring Generative AI: {e}")
    st.stop()

# Inisialisasi session state (tidak ada perubahan)
placeholder_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"
placeholder_caption = ""
placeholder_analysis = "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati dan mendapatkan rekomendasi."

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = placeholder_analysis
    st.session_state.image_urls = [placeholder_url] * 4
    st.session_state.image_captions = [placeholder_caption] * 4
    st.session_state.last_photo = None


# --- BAGIAN HEADER & KAMERA ---
st.markdown("""
<div class="logo-container">
    <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/35thn_logo.png" class="logo-35thn" />
    <div class="powered-by-container">
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png" class="logo-bakrieland" />
        <br>
        <span>POWERED BY:</span>
        <br>
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png" />
        <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png" />
    </div>
</div>

<div class="mascot-container">
    <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/mascot_logo.png" />
</div>
""", unsafe_allow_html=True)


# Layout Kamera dengan Overlay
st.markdown('<div class="camera-container">', unsafe_allow_html=True)
st.markdown('<div class="camera-overlay"></div>', unsafe_allow_html=True)
user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")
st.markdown('</div>', unsafe_allow_html=True)


# Proses gambar (tidak ada perubahan pada logic ini)
if user_input is not None and user_input != st.session_state.last_photo:
    st.session_state.last_photo = user_input
    with st.spinner("Menganalisis suasana hati Anda..."):
        try:
            image = Image.open(io.BytesIO(user_input.getvalue()))
            # ... (sisa logic pemrosesan Anda tetap sama)
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
    st.session_state.last_photo = None
    st.session_state.analysis_result = placeholder_analysis
    st.session_state.image_urls = [placeholder_url] * 4
    st.session_state.image_captions = [placeholder_caption] * 4
    st.rerun()


# --- BAGIAN MOOD ANALYTIC ---
escaped_analysis = html.escape(st.session_state.analysis_result)
st.markdown(f"""
<div class="canva-frame-container">
    <div class="canva-frame-content">
        <div class="canva-frame-title">MOOD ANALYTIC</div>
        <pre style="white-space: pre-wrap; font-family: inherit; color: #E0E0E0; background: none; border: none;">{escaped_analysis}</pre>
    </div>
</div>
""", unsafe_allow_html=True)


# --- BAGIAN REKOMENDASI ---
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div class="canva-frame-container">
        <div class="canva-frame-content recommendation-box">
            <div class="canva-frame-title">PROPERTY RECOMMENDATION</div>
            <img src="{st.session_state.image_urls[0]}" />
            <p>{st.session_state.image_captions[0]}</p>
            <img src="{st.session_state.image_urls[1]}" />
            <p>{st.session_state.image_captions[1]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="canva-frame-container">
        <div class="canva-frame-content recommendation-box">
            <div class="canva-frame-title">HOLIDAY RECOMMENDATION</div>
            <img src="{st.session_state.image_urls[2]}" />
            <p>{st.session_state.image_captions[2]}</p>
            <img src="{st.session_state.image_urls[3]}" />
            <p>{st.session_state.image_captions[3]}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- PENUTUP WRAPPER ---
st.markdown('</div>', unsafe_allow_html=True)


# --- Tombol Screenshot (tidak ada perubahan) ---
components.html("""
<html>
<head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
</head>
<body>
    <button id="screenshotBtn" style="
        position: fixed; bottom: 20px; right: 20px; z-index: 9999;
        background-color: #00c0cc; color: white; border: none;
        padding: 10px 20px; font-size: 16px; border-radius: 8px;
        cursor: pointer; box-shadow: 0 4px 12px rgba(0, 240, 255, 0.6);
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