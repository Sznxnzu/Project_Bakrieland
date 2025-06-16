import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io, html, random, qrcode, uuid, json, base64

# Import dan konfigurasi Firebase
import firebase_admin
from firebase_admin import credentials, db

# Konfigurasi halaman (hanya sekali di paling atas)
st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# Inisialisasi Firebase (hanya sekali per sesi)
@st.cache_resource
def initialize_firebase():
    try:
        if not firebase_admin._apps:
            service_account_info = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(cred, {'databaseURL': st.secrets["FIREBASE_URL"]})
        return True
    except Exception as e:
        st.error(f"Gagal menginisialisasi Firebase: {e}")
        return False

FIREBASE_INITIALIZED = initialize_firebase()

# --- Definisi Prompt Utama yang Baru dan Lebih Andal ---
MASTER_PROMPT = """
Analisis gambar wajah yang diberikan untuk menentukan mood atau suasana hati orang tersebut. 
Berikan analisis mendalam dalam beberapa kalimat.
Berdasarkan analisis mood tersebut, berikan 2 rekomendasi properti dan 2 rekomendasi liburan dari daftar yang disediakan.

Daftar Properti: Bogor Nirwana Residence, Kahuripan Nirwana, Sayana Bogor, Taman Rasuna Epicentrum, The Masterpiece & The Empyreal.
Daftar Liburan: Aston Bogor, Bagus Beach Walk, Grand ELTY Krakatoa, Hotel Aston Sidoarjo, Jungleland, Junglesea Kalianda, Rivera, Swiss Belresidences Rasuna Epicentrum, The Alana Malioboro, The Grove Suites, The Jungle Waterpark.

Kembalikan hasilnya HANYA dalam format JSON yang valid tanpa tambahan teks lain.
Struktur JSON harus seperti ini:
{
  "analysis_text": "Teks analisis mood Anda di sini...",
  "property_recs": ["Nama Properti 1", "Nama Properti 2"],
  "holiday_recs": ["Nama Liburan 1", "Nama Liburan 2"]
}
"""

def display_mobile_results(session_id):
    """Menampilkan halaman hasil untuk perangkat mobile."""
    if not FIREBASE_INITIALIZED: return

    # ... (Kode CSS dan HTML untuk halaman mobile bisa disalin dari versi sebelumnya, tidak ada perubahan) ...
    st.markdown("""<style>...</style>""", unsafe_allow_html=True)
    
    try:
        ref = db.reference(f'/{session_id}')
        results = ref.get()
        if not results:
            st.error("Hasil tidak ditemukan."); return

        st.markdown('<div id="capture-area" class="result-container">', unsafe_allow_html=True)
        st.image(base64.b64decode(results['user_photo_b64']), use_column_width=True, caption="Foto Anda")
        escaped_analysis = html.escape(results['analysis_text'])
        st.markdown(f"""<div class="mood-box-content"><h2>Mood Analytic</h2><pre style="white-space: pre-wrap; font-family: inherit;">{escaped_analysis}</pre></div>""", unsafe_allow_html=True)
        st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.image(results['image_urls'][0], caption=results['property_recs'][0])
        st.image(results['image_urls'][1], caption=results['property_recs'][1])
        st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.image(results['image_urls'][2], caption=results['holiday_recs'][0])
        st.image(results['image_urls'][3], caption=results['holiday_recs'][1])
        st.markdown('</div>', unsafe_allow_html=True)

        components.html(f"""...""", height=100) # Kode JS untuk download PDF
    except Exception as e:
        st.error(f"Gagal memuat hasil."); st.exception(e)


def run_main_app():
    """Menjalankan aplikasi utama."""
    if not FIREBASE_INITIALIZED: return

    # ... (Kode CSS Anda, tidak diubah) ...
    st.markdown("""<style>...</style>""", unsafe_allow_html=True)

    try:
        genai.configure(api_key=st.secrets["gemini_api"])
        model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        st.error(f"Error configuring Generative AI: {e}"); st.stop()

    if "app_status" not in st.session_state:
        st.session_state.app_status = {
            "analysis_result": "Arahkan kamera ke wajah Anda...",
            "image_urls": ["https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"] * 4,
            "image_captions": [""] * 4,
            "last_photo": None, "analysis_done": False, "session_id": None
        }

    # --- UI Utama ---
    row1 = st.container()
    with row1:
        colA1, colA2, colA3 = st.columns([0.2, 0.6, 0.2])
        with colA1: # Logo Kiri
            st.markdown("""<div class="column-wrapper"><div class="35thn-box"><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/35thn_logo.png" /></div><div class="mascot-box"><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/mascot_logo.png" /></div></div>""", unsafe_allow_html=True)
        with colA2: # Kamera
            user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed", key="camera")
        with colA3: # Logo Kanan
             st.markdown("""<div><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/bakrieland_logo.png" style="height: 70px; margin-bottom: 4px;" /></div><div><span style="display: inline-block; vertical-align: middle;"><div>POWERED BY:</div></span></div><div><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/google_logo.png" style="height: 40px; vertical-align: middle; margin-left: -10px; margin-right: -30px;" /><img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/metrodata_logo.png" style="height: 40px; vertical-align: middle;" /></div>""", unsafe_allow_html=True)

    # --- Logika Setelah Foto Diambil ---
    if user_input and user_input != st.session_state.app_status["last_photo"]:
        st.session_state.app_status["last_photo"] = user_input
        with st.spinner("Menganalisis suasana hati Anda..."):
            try:
                image = Image.open(io.BytesIO(user_input.getvalue()))
                user_photo_bytes = user_input.getvalue()
                
                # --- SATU PANGGILAN AI YANG LEBIH ANDAL ---
                response = model.generate_content([MASTER_PROMPT, image])
                
                # Membersihkan dan mem-parsing output JSON dari AI
                clean_json_str = response.text.strip().replace("```json", "").replace("```", "")
                parsed_result = json.loads(clean_json_str)

                # Mengambil data dari JSON yang sudah diparsing
                analysis_text = parsed_result["analysis_text"]
                property_recs = parsed_result["property_recs"]
                holiday_recs = parsed_result["holiday_recs"]
                
                # Fungsi untuk mendapatkan URL gambar (sama seperti sebelumnya)
                def get_image_url(name, category):
                    # Logika randomisasi nama file Anda
                    target_names = { "property": ["Bogor Nirwana Residence", "Kahuripan Nirwana", "Sayana Bogor", "Taman Rasuna Epicentrum", "The Masterpiece & The Empyreal"], "holiday": ["Aston Bogor", "Bagus Beach Walk", "Grand ELTY Krakatoa", "Hotel Aston Sidoarjo", "Jungleland", "Junglesea Kalianda", "Rivera", "Swiss Belresidences Rasuna Epicentrum", "The Alana Malioboro", "The Grove Suites", "The Jungle Waterpark"]}
                    if name in target_names[category]:
                        name = f"{name} {random.randint(1, 2)}"
                    return f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/{category}/{name.strip()}.jpg"

                image_urls = [get_image_url(p, "property") for p in property_recs] + [get_image_url(h, "holiday") for h in holiday_recs]
                
                session_id = str(uuid.uuid4())
                results_data = {
                    "user_photo_b64": base64.b64encode(user_photo_bytes).decode('utf-8'),
                    "analysis_text": analysis_text,
                    "property_recs": property_recs,
                    "holiday_recs": holiday_recs,
                    "image_urls": image_urls
                }
                
                db.reference(f'/{session_id}').set(results_data)

                # Memperbarui session state
                st.session_state.app_status.update({
                    "analysis_done": True, "session_id": session_id,
                    "analysis_result": analysis_text, "image_urls": image_urls,
                    "image_captions": property_recs + holiday_recs
                })

            except Exception as e:
                st.error("Gagal menganalisis gambar. Coba lagi dengan pencahayaan yang lebih baik.")
                st.exception(e) # Ini akan menampilkan detail error untuk debugging
                st.session_state.app_status["analysis_done"] = False
        st.rerun()
    
    # --- Tampilan Hasil ---
    escaped_analysis = html.escape(st.session_state.app_status["analysis_result"])
    st.markdown(f"""<div class="mood-box-content"><h2>Mood Analytic</h2><pre style="white-space: pre-wrap; font-family: inherit;">{escaped_analysis}</pre></div>""", unsafe_allow_html=True)
    
    colC1, colC2 = st.columns(2)
    urls = st.session_state.app_status["image_urls"]
    captions = st.session_state.app_status["image_captions"]
    with colC1:
        st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""<div class="portrait-box"><img src="{urls[0]}"/><p>{captions[0]}</p><img src="{urls[1]}"/><p>{captions[1]}</p></div>""", unsafe_allow_html=True)
    with colC2:
        st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""<div class="portrait-box"><img src="{urls[2]}"/><p>{captions[2]}</p><img src="{urls[3]}"/><p>{captions[3]}</p></div>""", unsafe_allow_html=True)

    # --- Tampilan QR Code (hanya jika analisis berhasil) ---
    if st.session_state.app_status["analysis_done"]:
        st.markdown("---")
        qr_col, mascot_col = st.columns([0.4, 0.6])
        with qr_col:
            st.markdown('<div class="header-box">Scan untuk Melihat & Download PDF</div>', unsafe_allow_html=True)
            base_url = "https://xxgwueozt6kgv6d8fzin5y.streamlit.app"
            full_url = f"{base_url}?session_id={st.session_state.app_status['session_id']}"
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(full_url); qr.make(fit=True)
            img = qr.make_image(fill_color="cyan", back_color="#19307f")
            buf = io.BytesIO(); img.save(buf, format="PNG")
            st.image(buf, width=250)
        with mascot_col:
            components.html("""...""", height=320) # Lottie Player Anda

# --- Router Utama Aplikasi ---
if "session_id" in st.query_params:
    display_mobile_results(st.query_params.get("session_id"))
else:
    run_main_app()