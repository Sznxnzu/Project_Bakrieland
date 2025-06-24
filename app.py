import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import random
import base64

st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# --- KODE HTML & JAVASCRIPT UNTUK TANGKAPAN LAYAR ---
CLIENT_SIDE_SCREEN_CAPTURE_HTML = """
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<style>
    #captureBtn {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        background-color: #00c0cc;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        font-family: 'sans-serif';
        border-radius: 8px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 240, 255, 0.6);
        transition: all 0.2s ease-in-out;
    }
    #captureBtn:hover {
        background-color: #00aabb;
        transform: scale(1.05);
    }
    #captureBtn:active {
        transform: scale(0.95);
    }
    #status-message {
        position: fixed;
        bottom: 80px;
        right: 20px;
        z-index: 9999;
        background-color: rgba(0, 0, 0, 0.7);
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 14px;
        font-family: 'sans-serif';
        display: none; /* Sembunyi secara default */
    }
</style>
<button id="captureBtn">📸 Ambil Screenshot</button>
<div id="status-message"></div>

<script>
    const captureButton = document.getElementById('captureBtn');
    const statusMessage = document.getElementById('status-message');

    function showStatus(message) {
        statusMessage.innerText = message;
        statusMessage.style.display = 'block';
        setTimeout(() => { statusMessage.style.display = 'none'; }, 3000);
    }

    captureButton.onclick = async () => {
        showStatus("Menyiapkan screenshot... ⏳");
        captureButton.style.display = 'none';
        await new Promise(r => setTimeout(r, 50)); 
        
        try {
            const canvas = await html2canvas(window.parent.document.body, {
                scale: window.devicePixelRatio,
                logging: false,
                useCORS: true,
                onclone: (clonedDoc) => {
                    const clonedButton = clonedDoc.getElementById('captureBtn');
                    if (clonedButton) {
                        clonedButton.style.display = 'none';
                    }
                }
            });

            const imageDataUrl = canvas.toDataURL('image/png');
            window.parent.Streamlit.setComponentValue(imageDataUrl);

        } catch (err) {
            showStatus(`Error: ${err.message}`);
            window.parent.Streamlit.setComponentValue(null);
        } finally {
            captureButton.style.display = 'block';
        }
    };
</script>
"""

# --- CSS STYLES ---
st.markdown("""
<style>
/* Gaya dasar dan tema */
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
/* CSS lainnya tidak berubah... */
</style>
""", unsafe_allow_html=True) # Tambahkan CSS Anda yang lain di sini jika perlu


# --- LOGIC & LAYOUT ---
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
if "screenshot_data" not in st.session_state:
    st.session_state.screenshot_data = None

# ... (Seluruh kode layout Anda dari row1, row2, row3 tetap sama) ...

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


# --- IMPLEMENTASI FITUR SCREENSHOT ---

# 1. Tampilkan komponen HTML/JS dan tangkap data yang dikirim kembali
screenshot_data_url = components.html(
    CLIENT_SIDE_SCREEN_CAPTURE_HTML,
    height=0 # Komponen tidak perlu tinggi karena tombolnya 'fixed'
)

# 2. Proses data HANYA JIKA ada data baru yang masuk dari JavaScript
if screenshot_data_url:
    # Simpan data ke session state agar tidak hilang saat rerun
    st.session_state.screenshot_data = screenshot_data_url
    # Lakukan rerun agar blok di bawah ini bisa menampilkan tombol download
    st.rerun()

# 3. Tampilkan tombol download JIKA data screenshot sudah ada di session state
if st.session_state.screenshot_data:
    try:
        # Hapus header 'data:image/png;base64,' dari string
        encoded_data = st.session_state.screenshot_data.split(",", 1)[1]
        # Decode string base64 menjadi bytes
        image_bytes = base64.b64decode(encoded_data)

        # Buat container untuk menempatkan tombol download di lokasi yang lebih baik
        # Kita gunakan kolom agar tidak mengganggu layout utama
        _, col_btn, _ = st.columns([0.4, 0.2, 0.4])
        with col_btn:
             # Tampilkan pratinjau kecil
            st.image(image_bytes, caption="Pratinjau Screenshot", width=200)
            
            # Buat tombol unduh yang sesungguhnya dengan data gambar
            st.download_button(
                label="💾 Unduh Hasil Screenshot",
                data=image_bytes,
                file_name="hasil_mood_analytic.png",
                mime="image/png",
                use_container_width=True
            )
        
        # Setelah tombol ditampilkan, reset data di session state agar tombol hilang lagi
        # dan siap untuk screenshot berikutnya.
        st.session_state.screenshot_data = None

    except Exception as e:
        st.error(f"Terjadi kesalahan saat memproses screenshot: {e}")
        st.session_state.screenshot_data = None