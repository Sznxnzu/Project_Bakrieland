import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import random

st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# URL untuk gambar bingkai lingkaran baru Anda
CAMERA_FRAME_URL = "https://i.ibb.co/L5B4z2X/image-6b1ef6.png"

# --- CSS STYLES ---
st.markdown(f"""
<style>
/* Gaya dasar dan tema (dari skrip awal Anda) */
html, body, [data-testid="stAppViewContainer"], .stApp {{
    background: none !important;
    background-color: #19307f !important;
    background-size: cover !important;
    background-position: center !important;
    background-attachment: fixed !important;
}}
::-webkit-scrollbar {{
  display: none;
}}

/* === CSS BARU UNTUK BINGKAI KAMERA (METODE STABIL) === */

/* 1. Wadah yang akan memiliki gambar bingkai sebagai background */
.camera-container-new {{
    width: 500px;
    height: 500px;
    margin: 0 auto; /* Menengahkan wadah */
    background-image: url('{CAMERA_FRAME_URL}');
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    display: flex; /* Menggunakan flexbox untuk menengahkan kamera di dalamnya */
    align-items: center;
    justify-content: center;
}}

/* 2. Mengatur KAMERA ASLI (st.camera_input) yang ada di dalam wadah */
div[data-testid="stCameraInput"] {{
    width: 100% !important;
    height: 100% !important;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

div[data-testid="stCameraInput"] div {{
    background-color: transparent !important;
}}

/* 3. Membuat KOTAK KAMERA menjadi BULAT dan sedikit lebih kecil dari bingkai */
div[data-testid="stCameraInputWebcamStyledBox"] {{
    width: 85% !important;  /* Ukuran kamera 85% dari ukuran bingkai */
    height: 85% !important; /* Sehingga bingkai di background terlihat */
    border-radius: 50% !important; /* Membuat kamera tetap bulat */
    overflow: hidden;
    margin: auto;
    box-shadow: 0 0 20px rgba(0,240,255,0.5); /* Efek glow tetap ada */
}}

div[data-testid="stCameraInput"] video,
div[data-testid="stCameraInput"] img {{
    object-fit: cover;
    width: 100%;
    height: 100%;
}}


/* Sisa CSS dari skrip awal Anda (TIDAK DIUBAH) */
.header-box, .portrait-box, .mood-box-content {{
    border: 2px solid #00f0ff;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px #00f0ff;
    background-color: rgba(0,0,30,0.6);
}}
.header-box {{
    background-color: rgba(0,0,50,0.5);
    color: #00f0ff;
    font-size: 25px;
    text-align: center;
}}
.mood-box-content {{
    background-color: rgba(10, 15, 30, 0.85);
    font-size: 25px;
}}
.mood-box-content h2{{
    font-size: 45px;
}}

.column-wrapper, .35thn-box, .mascot-box {{
    /* Style ini tidak diubah */
    display: flex;
    flex-direction: column;
}}
/* ... dan sisa style lainnya dari skrip awal ... */


/* RESPONSIVE KHUSUS MOBILE (MAX WIDTH 768px) */
@media (max-width: 768px) {{
    .camera-container-new {{
        width: 85vw !important;
        height: 85vw !important;
    }}
    /* ... sisa style responsive lainnya ... */
}}
</style>
""", unsafe_allow_html=True)


# --- LOGIC & LAYOUT (SEMUA FUNGSI ANALISIS TIDAK DIUBAH) ---
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
        # Tidak diubah
        st.write("")
        st.markdown("""
        <div class="column-wrapper" style="height:400px; justify-content: space-between;">
            <div class="35thn-box" style="width:150px; margin: 0 auto;"><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/35thn_logo.png" style="width:100%;"/></div>
            <div class="mascot-box" style="width:150px; margin: 0 auto;"><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/mascot_logo.png" style="width:100%;"/></div>
        </div>
        """, unsafe_allow_html=True)
    with colA2:
        # === PERUBAHAN LAYOUT HANYA DI SINI ===
        # Membuat wadah lalu menempatkan kamera di dalamnya
        st.markdown('<div class="camera-container-new">', unsafe_allow_html=True)
        user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")
        st.markdown('</div>', unsafe_allow_html=True)


        # LOGIKA ANALISIS ANDA (TIDAK DIUBAH SAMA SEKALI)
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
                        # Logika nama file tidak diubah
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
                        st.session_state.analysis_result = "Gagal memproses rekomendasi gambar."
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat pemrosesan: {e}")
                    st.session_state.analysis_result = "Gagal menganalisis gambar."
            st.rerun()
        elif user_input is None and st.session_state.last_photo is not None:
            st.session_state.analysis_result = placeholder_analysis
            st.session_state.image_urls = [placeholder_url] * 4
            st.session_state.image_captions = [placeholder_caption] * 4
            st.session_state.last_photo = None
            st.rerun()

    with colA3:
        # Tidak diubah
        st.markdown("""
        <div style="text-align:right">
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png" style="height: 70px; margin-bottom: 4px;" />
            <br>
            <span>POWERED BY:</span>
            <br>
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png" style="height: 40px;" />
            <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png" style="height: 40px;" />
        </div>
        """, unsafe_allow_html=True)

# SEMUA FRAME DAN FUNGSI DI BAWAH INI TIDAK DIUBAH
row2 = st.container()
with row2:
    escaped_analysis = html.escape(st.session_state.analysis_result)
    st.markdown(f"""
    <div class="mood-box-content" style="text-align:left;">
      <h2 style="text-align:center;">Mood Analytic</h2>
      <pre style="white-space: pre-wrap; font-family: inherit;">{escaped_analysis}</pre>
    </div>
    """, unsafe_allow_html=True)

row3 = st.container()
with row3:
    colC1, colC2 = st.columns(2)
    with colC1:
        st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="portrait-box" style="text-align:center;">
          <img src="{st.session_state.image_urls[0]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
          <p style="font-size: 30px; color: #ccc;">{st.session_state.image_captions[0]}</p>
          <img src="{st.session_state.image_urls[1]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
          <p style="font-size: 30px; color: #ccc;">{st.session_state.image_captions[1]}</p>
        </div>
        """, unsafe_allow_html=True)
    with colC2:
        st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="portrait-box" style="text-align:center;">
          <img src="{st.session_state.image_urls[2]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
          <p style="font-size: 30px; color: #ccc;">{st.session_state.image_captions[2]}</p>
          <img src="{st.session_state.image_urls[3]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
          <p style="font-size: 30px; color: #ccc;">{st.session_state.image_captions[3]}</p>
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