import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import random

st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# URL untuk gambar bingkai kamera baru Anda
# Pastikan URL ini benar dan diakhiri dengan ?raw=true
CAMERA_FRAME_URL = "https://github.com/husnanali05/FP_Datmin/blob/main/Halaman%20Story%20WA%20(1).png?raw=true"


# --- CSS STYLES ---
st.markdown(f"""
<style>
/* Gaya dasar dan tema (dari skrip awal Anda) */
html, body, [data-testid="stAppViewContainer"], .stApp {{
    background: none !important;
    background-color: #19307f !important;
}}
::-webkit-scrollbar {{
  display: none;
}}

.header-box, .portrait-box, .mood-box-content {{
    border: 2px solid #00f0ff;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
    text-align: center;
}}

/* === BAGIAN PENTING UNTUK BINGKAI KAMERA BARU === */

/* 1. Wadah untuk menampung Kamera dan Bingkai secara bertumpuk */
.camera-frame-container {{
    position: relative; /* Membuat posisi absolut di dalamnya bekerja */
    width: 500px; /* Lebar total area kamera */
    height: 500px; /* Tinggi total area kamera */
    margin: 0 auto; /* Menengahkan wadah */
}}

/* 2. Lapisan (Overlay) untuk BINGKAI dari URL Anda */
.camera-frame-overlay {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('{CAMERA_FRAME_URL}');
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    pointer-events: none; /* Penting! Agar bingkai tidak bisa diklik */
    z-index: 5; /* Memastikan bingkai ada di atas kamera */
}}

/* 3. Menyesuaikan posisi KAMERA ASLI (st.camera_input) di dalam wadah */
div[data-testid="stCameraInput"] {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100% !important;
    height: 100% !important;
    z-index: 1; /* Kamera ada di lapisan bawah */
}}

/* Menghapus style lingkaran bawaan agar tidak bentrok dengan bingkai baru */
div[data-testid="stCameraInputWebcamStyledBox"],
div[data-testid="stCameraInput"] img {{
    border-radius: 0 !important;
    box-shadow: none !important;
}}
/* ========================================================= */


/* Sisa CSS dari skrip awal Anda */
.column-wrapper {{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 400px;
}}
.35thn-box, .mascot-box {{
  width: 150px;
  margin: 0 auto;
}}
.35thn-box img, .mascot-box img {{
  width: 100%;
}}

/* RESPONSIVE KHUSUS MOBILE */
@media (max-width: 768px) {{
    .camera-frame-container {{
        width: 85vw !important;
        height: 85vw !important;
    }}
    .column-wrapper {{
        flex-direction: row;
        height: auto;
        align-items: center;
        justify-content: space-around;
        margin-bottom: 20px;
    }}
}}
</style>
""", unsafe_allow_html=True)


# --- LOGIC & LAYOUT (dari skrip awal Anda) ---
# Bagian ini tidak diubah, semua logika AI dan rekomendasi tetap sama.
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
        # === PERUBAHAN LAYOUT UNTUK MENERAPKAN BINGKAI BARU ===
        st.markdown("""
        <div class="camera-frame-container">
            <div class="camera-frame-overlay"></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Menempatkan kamera di dalam wadah secara logis.
        # Streamlit akan menempatkan widget ini di dalam container di atasnya.
        # KAMERA INI TIDAK HILANG, HANYA DITUMPUK DENGAN BINGKAI.
        user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")


        if user_input is not None and user_input != st.session_state.last_photo:
            st.session_state.last_photo = user_input

            with st.spinner("Menganalisis suasana hati Anda..."):
                # ... (Logika analisis Anda yang lain tetap sama) ...
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

                        first_target_names = ["Bogor Nirwana Residence", "Kahuripan Nirwana", "Sayana Bogor", "Taman Rasuna Epicentrum", "The Masterpiece & The Empyreal"]
                        first_filenames_edited = [name.strip() + " " + str(random.randint(1, 2)) if name.strip() in first_target_names else name.strip() for name in first_filenames]

                        second_target_names = ["Aston Bogor", "Bagus Beach Walk", "Grand ELTY Krakatoa", "Hotel Aston Sidoarjo", "Jungleland", "Junglesea Kalianda", "Rivera", "Swiss Belresidences Rasuna Epicentrum", "The Alana Malioboro", "The Grove Suites", "The Jungle Waterpark"]
                        second_filenames_edited = [name.strip() + " " + str(random.randint(1, 2)) if name.strip() in second_target_names else name.strip() for name in second_filenames]

                        st.session_state.image_urls = [
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{first_filenames_edited[0].strip()}.jpg",
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{first_filenames_edited[1].strip()}.jpg",
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{second_filenames_edited[0].strip()}.jpg",
                            f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{second_filenames_edited[1].strip()}.jpg"
                        ]
                        st.session_state.image_captions = [first_filenames[0].strip(), first_filenames[1].strip(), second_filenames[0].strip(), second_filenames[1].strip()]
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
        # ... (Kode kolom kanan Anda tidak berubah) ...
        st.markdown("""
        <div><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png" style="height: 70px; margin-bottom: 4px;" /></div>
        <div><span>POWERED BY:</span></div>
        <div>
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png" style="height: 40px; vertical-align: middle; margin-left: -10px; margin-right: -30px;" />
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png" style="height: 40px; vertical-align: middle;" />
        </div>
        """, unsafe_allow_html=True)

# Sisa dari layout (row2, row3, components.html) tidak diubah dan tetap sama
# ... (tempel sisa kode row2, row3, dan components.html dari skrip asli Anda di sini)
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
    <button id="screenshotBtn" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">📸 Screenshot</button>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
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
    """, height=0)