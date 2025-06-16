# Import yang diperlukan
import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io, os, html, random, uuid, base64, json

# Import dan konfigurasi Firebase
import firebase_admin
from firebase_admin import credentials, db

# --- Fungsi Inisialisasi Firebase ---
# Menggunakan @st.cache_resource agar koneksi hanya dibuat sekali.
@st.cache_resource
def initialize_firebase():
    try:
        # Cek apakah aplikasi sudah diinisialisasi
        if not firebase_admin._apps:
            # Ambil credentials dari Streamlit Secrets
            service_account_info = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
            cred = credentials.Certificate(service_account_info)
            
            # Inisialisasi aplikasi Firebase
            firebase_admin.initialize_app(cred, {
                'databaseURL': st.secrets["FIREBASE_URL"]
            })
        return True
    except Exception as e:
        st.error(f"Gagal menginisialisasi Firebase: {e}")
        return False

# Panggil fungsi inisialisasi di awal
FIREBASE_INITIALIZED = initialize_firebase()

# --- Fungsi untuk halaman mobile ---
def display_mobile_results(session_id):
    if not FIREBASE_INITIALIZED:
        st.error("Koneksi ke database gagal. Tidak dapat memuat hasil.")
        return

    st.markdown("""<style>...</style>""", unsafe_allow_html=True) # CSS Anda di sini untuk mempersingkat

    try:
        # Muat data dari Firebase Realtime Database
        ref = db.reference(f'/{session_id}')
        results = ref.get()
        
        if not results:
            st.error("Hasil tidak ditemukan atau sudah kedaluwarsa.")
            st.info("Sesi ini mungkin sudah lama. Silakan pindai ulang QR code yang baru.")
            return

        # Area yang akan diubah menjadi PDF
        st.markdown('<div id="capture-area" class="result-container">', unsafe_allow_html=True)
        st.image(base64.b64decode(results['user_photo_b64']), use_column_width=True, caption="Foto Anda")
        escaped_analysis = html.escape(results['analysis_result'])
        st.markdown(f"""...""", unsafe_allow_html=True) # HTML Mood Box Anda di sini
        st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.image(results['image_urls'][0], caption=results['image_captions'][0])
        st.image(results['image_urls'][1], caption=results['image_captions'][1])
        st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.image(results['image_urls'][2], caption=results['image_captions'][2])
        st.image(results['image_urls'][3], caption=results['image_captions'][3])
        st.markdown('</div>', unsafe_allow_html=True)

        # Komponen HTML untuk download PDF (tidak berubah)
        components.html(f"""...""", height=100) # Kode HTML/JS Anda untuk PDF di sini
    
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat hasil dari Firebase: {e}")

# --- Fungsi untuk aplikasi utama ---
def run_main_app():
    if not FIREBASE_INITIALIZED:
        st.error("Koneksi ke database gagal. Aplikasi tidak dapat berfungsi.")
        return
        
    # CSS Anda, Konfigurasi Gemini, session_state, dll. (tidak berubah)
    # ...
    # ...

    # Di dalam blok 'if user_input is not None':
    # ...
    # Setelah Anda mendapatkan semua hasil analisis:
    try:
        # ... (logika analisis Anda)
        if len(filenames) >= 4:
            # ... (logika pemrosesan nama file Anda)

            session_id = str(uuid.uuid4())
            results_data = {
                "user_photo_b64": base64.b64encode(user_photo_bytes).decode('utf-8'),
                "analysis_result": raw_output,
                "image_urls": image_urls,
                "image_captions": image_captions
            }
            
            # <<< PERUBAHAN UTAMA: Simpan hasil ke Firebase, bukan file lokal >>>
            ref = db.reference(f'/{session_id}')
            ref.set(results_data)
            
            st.session_state.analysis_done = True
            st.session_state.session_id = session_id
            st.session_state.results_data = results_data
        else:
            # ...
    except Exception as e:
        # ...
    # ... sisa kode Anda ...
    
    # Di bagian pembuatan QR Code:
    if st.session_state.analysis_done:
        # ...
        # Pastikan base_url menggunakan URL publik Streamlit Anda
        base_url = "https://xxgwueozt6kgv6d8fzin5y.streamlit.app"
        full_url = f"{base_url}?session_id={st.session_state.session_id}"
        # ... (sisa logika QR code)

# --- Router Utama ---
# Kode debug sementara bisa dihapus atau diberi komentar
# st.write("Parameter URL yang diterima:", st.query_params)

query_params = st.query_params
if "session_id" in query_params:
    session_id_from_url = query_params["session_id"]
    # Periksa apakah session_id adalah string tunggal, bukan list
    if isinstance(session_id_from_url, list):
        session_id_from_url = session_id_from_url[0]
    display_mobile_results(session_id_from_url)
else:
    run_main_app()