import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import random

st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# --- CSS STYLES ---
# Perubahan untuk responsivitas logo dan kamera ada di sini
st.markdown("""
<style>
/* --- Gaya Dasar (Desktop) --- */
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
.portrait-box {
    border: 2px solid #00f0ff;
    background-color: rgba(0,0,30,0.6);
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
    box-shadow: 0 0 10px #00f0ff;
    text-align: center;
}

.column-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%; /* Dibuat fleksibel */
  min-height: 450px; /* Jaga tinggi minimal */
}

/* PERUBAHAN 1: Logo dibuat responsif di desktop */
.35thn-box, .mascot-box {
  width: 80%;             /* Gunakan persentase dari kolomnya */
  max-width: 150px;       /* Batasi ukuran maksimal agar tidak terlalu besar */
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
}
.mascot-box {
    height: auto;
}
.35thn-box img, .mascot-box img {
  width: 100%;
  border-radius: 8px;
  vertical-align: top;
}


.mood-box-content {
    border: 2px solid #00f0ff;
    background-color: rgba(10, 15, 30, 0.85);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 20px #00f0ff;
    font-size: 25px;
    margin-top: 10px;
    margin-bottom: 10px;
    width: 100%;
    height: auto;
}
.mood-box-content h2{
    font-size: 45px
}

/* PERUBAHAN 2: Kamera dibuat responsif di desktop */
.camera-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}
div[data-testid="stCameraInput"] {
  width: 100% !important;     /* Gunakan 100% dari kolom tengah */
  height: auto !important;    /* Tinggi otomatis */
  max-width: 500px !important;/* Batasi ukuran maksimal */
  aspect-ratio: 1 / 1;      /* Paksa agar selalu berbentuk persegi */
  margin: 0 auto;
}
div[data-testid="stCameraInput"] div {
  background-color: transparent !important;
}
div[data-testid="stCameraInputWebcamStyledBox"], div[data-testid="stCameraInput"] img {
  width: 100% !important;
  height: 100% !important;
  border-radius: 50% !important; /* Membuatnya bulat */
  object-fit: cover;
  box-shadow: 0 0 20px rgba(0,240,255,0.5);
}
div[data-testid="stCameraInput"] button {
  z-index: 10;
  position: absolute;
  bottom: 5%; /* Posisi relatif */
  right: 5%;  /* Posisi relatif */
  width: 150px;
  background-color: #00c0cc;
  color: #000;
  font-weight: 600;
  font-size: 16px;
}
[data-testid="stCameraInputSwitchButton"] {
  display: none !important;
}


/* --- PENAMBAHAN: ATURAN RESPONSIVE UNTUK MOBILE & TABLET --- */
@media (max-width: 768px) {
    /* Mengatur ulang layout kolom utama untuk mobile */
    .st-emotion-cache-z5fcl4 {
        flex-direction: column;
    }

    /* Mengubah ukuran font agar tidak terlalu besar */
    .header-box { font-size: 18px; }
    .mood-box-content h2 { font-size: 30px; }
    .mood-box-content { font-size: 16px; }
    .portrait-box p { font-size: 18px !important; }

    /* PERUBAHAN 3: Kamera di mobile dibuat lebih dinamis */
    div[data-testid="stCameraInput"] {
        width: 80vw !important; /* 80% dari lebar layar */
        max-width: 300px !important; /* Batas maksimal */
    }

    /* Menyesuaikan posisi tombol kamera di mobile */
    div[data-testid="stCameraInput"] button {
        width: 120px;
        font-size: 14px;
        bottom: 10px;
        right: 50%;
        transform: translateX(50%); /* Pusatkan tombol */
    }

    /* Mengatur ulang kolom samping di mobile */
    .column-wrapper {
        flex-direction: row;
        height: auto;
        min-height: auto;
        align-items: center;
        justify-content: space-around;
        margin-bottom: 20px;
    }

    /* PERUBAHAN 4: Logo & Maskot dibuat responsif di mobile */
    .35thn-box, .mascot-box {
        width: 30%;             /* Ukuran relatif terhadap layar */
        max-width: 100px;       /* Batas ukuran maksimal */
        height: auto;
        margin: 0;
    }
    
    /* Menyesuaikan logo Bakrieland & powered by */
    img[src*="bakrieland_logo"] { height: 50px !important; }
    img[src*="google_logo"], img[src*="metrodata_logo"] { height: 30px !important; }

    /* Membuat kolom rekomendasi menjadi satu kolom */
    div[data-testid="stHorizontalBlock"] {
        flex-direction: column;
    }
}

</style>
""", unsafe_allow_html=True)


# --- BAGIAN LOGIC & LAYOUT PYTHON (TETAP SAMA) ---
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
        st.markdown('<div class="camera-wrapper">', unsafe_allow_html=True)
        user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")
        st.markdown('</div>', unsafe_allow_html=True)

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
<html>
  <head>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  </head>
  <body>
    <button id="screenshotBtn" style="
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        background-color: #00c0cc;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 8px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 240, 255, 0.6);
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