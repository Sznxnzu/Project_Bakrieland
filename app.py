import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import random
import qrcode
import uuid
import json
import base64

# Import dan konfigurasi Firebase
import firebase_admin
from firebase_admin import credentials, db

# Konfigurasi halaman diletakkan di bagian paling atas
st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

@st.cache_resource
def initialize_firebase():
    """Menginisialisasi koneksi ke Firebase menggunakan credentials dari Streamlit Secrets."""
    try:
        if not firebase_admin._apps:
            service_account_info = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred, {'databaseURL': st.secrets["FIREBASE_URL"]})
        return True
    except Exception as e:
        st.error(f"Gagal menginisialisasi Firebase. Pastikan Streamlit Secrets sudah dikonfigurasi. Error: {e}")
        return False

# Inisialisasi Firebase saat aplikasi dimuat
FIREBASE_INITIALIZED = initialize_firebase()

def display_mobile_results(session_id):
    """Fungsi untuk menampilkan halaman hasil di perangkat mobile dengan data dari Firebase."""
    if not FIREBASE_INITIALIZED: return

    # ... (Kode CSS dan HTML untuk halaman mobile bisa disalin dari versi sebelumnya) ...
    st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], .stApp { background-color: #19307f !important; }
        .result-container { padding: 20px; background-color: #19307f; color: white; border-radius: 10px; }
        .mood-box-content { border: 2px solid #00f0ff; background-color: rgba(10, 15, 30, 0.85); padding: 15px; border-radius: 10px; box-shadow: 0 0 20px #00f0ff; font-size: 15px; margin-top: 10px; margin-bottom: 20px; }
        .header-box { text-align: center; border: 2px solid #00f0ff; background-color: rgba(0,0,50,0.5); border-radius: 8px; padding: 10px; margin-bottom: 10px; box-shadow: 0 0 10px #00f0ff; color: #00f0ff; font-size: 20px; }
        img { max-width: 100%; border-radius: 8px; }
        .download-button { display: block; width: 100%; padding: 15px; margin-top: 20px; background-color: #00c0cc; color: #000; font-weight: bold; text-align: center; border: none; border-radius: 8px; cursor: pointer; text-decoration: none; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

    try:
        ref = db.reference(f'/{session_id}')
        results = ref.get()
        if not results:
            st.error("Hasil tidak ditemukan atau sudah kedaluwarsa.")
            st.info("Silakan pindai ulang QR code yang baru dari aplikasi utama.")
            return

        st.markdown('<div id="capture-area" class="result-container">', unsafe_allow_html=True)
        st.image(base64.b64decode(results['user_photo_b64']), use_column_width=True, caption="Foto Anda")
        escaped_analysis = html.escape(results['analysis_result'])
        st.markdown(f"""<div class="mood-box-content"><h2 style="font-size: 28px;">Mood Analytic</h2><pre style="white-space: pre-wrap; font-family: inherit;">{escaped_analysis}</pre></div>""", unsafe_allow_html=True)
        st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.image(results['image_urls'][0], caption=results['image_captions'][0])
        st.image(results['image_urls'][1], caption=results['image_captions'][1])
        st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.image(results['image_urls'][2], caption=results['image_captions'][2])
        st.image(results['image_urls'][3], caption=results['image_captions'][3])
        st.markdown('</div>', unsafe_allow_html=True)

        components.html(f"""
            <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
            <a id="downloadButton" class="download-button">Download Hasil sebagai PDF</a>
            <script>
                const {{ jsPDF }} = window.jspdf;
                document.getElementById('downloadButton').addEventListener('click', function() {{
                    const captureElement = document.getElementById('capture-area');
                    html2canvas(captureElement, {{ backgroundColor: '#19307f', useCORS: true, scale: 1.5 }}).then(canvas => {{
                        const imgData = canvas.toDataURL('image/png');
                        const pdfWidth = 210;
                        const pdfHeight = (canvas.height * pdfWidth) / canvas.width;
                        const pdf = new jsPDF({{ orientation: 'portrait', unit: 'mm', format: [pdfWidth, pdfHeight] }});
                        pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
                        pdf.save('hasil-analisis-bakrieland.pdf');
                    }});
                }});
            </script>
        """, height=100)
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat hasil dari Firebase:")
        st.exception(e)


def run_main_app():
    if not FIREBASE_INITIALIZED:
        st.warning("Menunggu koneksi ke database...")
        return
    
    # KODE CSS ANDA (tidak diubah)
    st.markdown("""<style>...</style>""", unsafe_allow_html=True)

    try:
        genai.configure(api_key=st.secrets["gemini_api"])
        model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"Error configuring Generative AI: {e}")
        st.stop()
    
    analysis_prompt = """
PASTIKAN ANDA MENEMPELKAN SELURUH ISI FILE 'prompt.txt' ANDA DI SINI.
"""
    json_prompt = """
PASTIKAN ANDA MENEMPELKAN SELURUH ISI FILE 'prompt_json.txt' ANDA DI SINI.
"""

    # Menggunakan nama session state yang berbeda untuk menghindari konflik
    if "app_status" not in st.session_state:
        st.session_state.app_status = {
            "analysis_result": "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati dan mendapatkan rekomendasi yang dipersonalisasi.",
            "image_urls": ["https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"] * 4,
            "image_captions": [""] * 4,
            "last_photo": None,
            "analysis_done": False,
            "session_id": None
        }

    row1 = st.container()
    with row1:
        colA1, colA2, colA3 = st.columns([0.2, 0.6, 0.2])
        with colA1:
            st.markdown("""...""", unsafe_allow_html=True) # Logo Kiri
        with colA2:
            user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")

            if user_input is not None and user_input != st.session_state.app_status["last_photo"]:
                st.session_state.app_status["last_photo"] = user_input
                with st.spinner("Menganalisis suasana hati Anda..."):
                    try:
                        st.toast("✅ Foto diterima. Memulai analisis AI...")
                        image = Image.open(io.BytesIO(user_input.getvalue()))
                        user_photo_bytes = user_input.getvalue()
                        
                        analysis_response = model.generate_content([analysis_prompt, image])
                        raw_output = analysis_response.text
                        
                        st.toast("✅ Analisis pertama selesai. Memformat ke JSON...")
                        json_response = model.generate_content([json_prompt, raw_output])
                        filenames = json_response.text.strip().split(",")
                        
                        st.toast("✅ Pemformatan JSON selesai. Memproses data...")
                        if len(filenames) >= 4:
                            midpoint = len(filenames) // 2
                            first_filenames, second_filenames = filenames[:midpoint], filenames[midpoint:]
                            first_target_names = ["Bogor Nirwana Residence", "Kahuripan Nirwana", "Sayana Bogor", "Taman Rasuna Epicentrum", "The Masterpiece & The Empyreal"]
                            first_filenames_edited = [f"{name.strip()} {random.randint(1, 2)}" if name.strip() in first_target_names else name.strip() for name in first_filenames]
                            second_target_names = ["Aston Bogor", "Bagus Beach Walk", "Grand ELTY Krakatoa", "Hotel Aston Sidoarjo", "Jungleland", "Junglesea Kalianda", "Rivera", "Swiss Belresidences Rasuna Epicentrum", "The Alana Malioboro", "The Grove Suites", "The Jungle Waterpark"]
                            second_filenames_edited = [f"{name.strip()} {random.randint(1, 2)}" if name.strip() in second_target_names else name.strip() for name in second_filenames]
                            image_urls = [f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{edited_name.strip()}.jpg" for edited_name in first_filenames_edited[:2]] + \
                                         [f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{edited_name.strip()}.jpg" for edited_name in second_filenames_edited[:2]]
                            image_captions = [name.strip() for name in first_filenames[:2]] + [name.strip() for name in second_filenames[:2]]
                            
                            session_id = str(uuid.uuid4())
                            results_data = {"user_photo_b64": base64.b64encode(user_photo_bytes).decode('utf-8'), "analysis_result": raw_output, "image_urls": image_urls, "image_captions": image_captions}
                            
                            st.toast("⏳ Menyimpan hasil ke database...")
                            ref = db.reference(f'/{session_id}'); ref.set(results_data)
                            st.toast("✅ Hasil berhasil disimpan!")

                            st.session_state.app_status["analysis_done"] = True
                            st.session_state.app_status["session_id"] = session_id
                            st.session_state.app_status["analysis_result"] = raw_output
                            st.session_state.app_status["image_urls"] = image_urls
                            st.session_state.app_status["image_captions"] = image_captions
                        else:
                            st.session_state.app_status["analysis_result"] = "Gagal memproses rekomendasi gambar. Silakan coba lagi."
                            st.session_state.app_status["analysis_done"] = False
                    
                    except Exception as e:
                        # Menampilkan error dengan lebih detail
                        st.error("Terjadi kesalahan fatal saat pemrosesan!")
                        st.exception(e)
                        st.session_state.app_status["analysis_result"] = "Gagal menganalisis gambar karena terjadi error."
                        st.session_state.app_status["analysis_done"] = False
                
                st.rerun()

            elif user_input is None and st.session_state.app_status["last_photo"] is not None:
                st.session_state.app_status["last_photo"] = None
                st.session_state.app_status["analysis_done"] = False
                st.session_state.app_status["analysis_result"] = "Arahkan kamera ke wajah Anda dan ambil foto untuk memulai analisis suasana hati dan mendapatkan rekomendasi yang dipersonalisasi."
                st.rerun()
        with colA3:
            st.markdown("""...""", unsafe_allow_html=True) # Logo Kanan

    row2 = st.container()
    with row2:
        escaped_analysis = html.escape(st.session_state.app_status["analysis_result"])
        st.markdown(f"""<div class="mood-box-content"><h2>Mood Analytic</h2><pre style="white-space: pre-wrap; font-family: inherit;">{escaped_analysis}</pre></div>""", unsafe_allow_html=True)

    row3 = st.container()
    with row3:
        colC1, colC2 = st.columns(2)
        with colC1:
            st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
            st.markdown(f"""<div class="portrait-box">...</div>""", unsafe_allow_html=True) # Rekomendasi 1
        with colC2:
            st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
            st.markdown(f"""<div class="portrait-box">...</div>""", unsafe_allow_html=True) # Rekomendasi 2

    if st.session_state.app_status["analysis_done"]:
        st.markdown("---")
        qr_col, mascot_col = st.columns([0.4, 0.6])
        with qr_col:
            st.markdown('<div class="header-box" style="font-size: 18px;">Scan untuk Melihat & Download PDF</div>', unsafe_allow_html=True)
            base_url = "https://xxgwueozt6kgv6d8fzin5y.streamlit.app" # URL Publik Anda
            full_url = f"{base_url}?session_id={st.session_state.app_status['session_id']}"
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
            qr.add_data(full_url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="cyan", back_color="#19307f")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.image(buf, width=250)
        with mascot_col:
            components.html("""...""", height=320) # Lottie Player

# --- Router Utama Aplikasi ---
query_params = st.query_params
if "session_id" in query_params:
    session_id_from_url = query_params.get("session_id")
    if isinstance(session_id_from_url, list):
        session_id_from_url = session_id_from_url[0]
    display_mobile_results(session_id_from_url)
else:
    run_main_app()