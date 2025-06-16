import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html
import random
import qrcode
import base64
import urllib.parse # Untuk encode URL parameter

st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

# --- CSS Styling --- (Tidak berubah, tetap sama seperti sebelumnya)
st.markdown("""
<style>
/* ... (CSS Anda yang sudah ada) ... */

/* Highlight the section to be screenshotted */
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
    position: relative;
    /* Added for clarity on what will be captured */
    outline: 2px solid rgba(255,255,0,0.5); /* Temporary: Highlight what will be captured */
    outline-offset: 5px;
}
.mood-box-content:hover {
    box-shadow: 0 0 25px #00f0ff, 0 0 50px #00f0ff;
}
.mood-box-content p {
    margin-bottom: 0;
}
.mood-box-content h2{
    font-size: 45px;
    color: #fff;
    text-align: center;
    margin-top: 0;
    margin-bottom: 15px;
}
.mood-box-content pre {
    color: #fff;
    font-size: 1.2em;
}
.mood-box-content ul {
    margin-top: 0;
    margin-bottom: 1em;
    padding-left: 20px;
}

/* ... (Sisa CSS Anda) ... */

/* Remove the download button style since it won't be explicitly clicked */
/* .stDownloadButton button { display: none; } */
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

        # --- QR Code Section for Download ---
        # Get the current app URL. For deployment, this needs to be known.
        # Example for Streamlit Cloud: "https://your-app-name.streamlit.app"
        # Example for local: "http://localhost:8501"
        
        # We need a unique way to identify the *current state* of the analysis
        # to ensure the QR code downloads *that specific result*.
        # For simplicity, we'll assume the URL will trigger a screenshot of the *currently displayed* result.
        # If you need to download a *specific historical* result, you'd need to store results server-side
        # and embed an ID in the QR code URL.

        # Mengambil query parameters saat ini untuk membangun URL yang tepat
        query_params = st.query_params.to_dict()
        # Jika Anda ingin QR code memicu unduhan, tambahkan parameter ke URL saat ini
        # Misalnya, jika aplikasi Anda diakses di `https://myapp.streamlit.app/`
        # QR code akan mengarah ke `https://myapp.streamlit.app/?download=true`
        
        # Dapatkan URL dasar aplikasi Anda. Ini mungkin perlu disesuaikan saat deploy.
        # Asumsi untuk testing lokal:
        base_url = "http://localhost:8501" # GANTI INI DENGAN URL ASLI APPLIKASI ANDA SAAT DI DEPLOY!
        
        # Pastikan kita tidak menambah parameter `download` jika sudah ada untuk menghindari loop
        download_url_params = query_params.copy()
        download_url_params["download_mood"] = "true" # Parameter yang akan memicu unduhan
        
        # Ubah dictionary parameter menjadi string query yang di-encode URL
        encoded_params = urllib.parse.urlencode(download_url_params)
        
        # Gabungkan base URL dengan parameter untuk QR code
        qr_data_url = f"{base_url}?{encoded_params}"

        # Debugging: tampilkan URL yang akan di-encode ke QR
        # st.write(f"QR Code will point to: {qr_data_url}")

        qr_image_bytes = generate_qr_code(qr_data_url)

        st.markdown(f"""
            <div class="qr-box">
                <img src="data:image/png;base64,{base64.b64encode(qr_image_bytes).decode('utf-8')}" alt="QR Code" />
                <p>Scan untuk mengunduh hasil analisis mood.</p>
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

    # --- Auto-trigger download based on URL parameter ---
    # Mendapatkan query parameters
    query_params = st.query_params

    # Cek apakah parameter 'download_mood' ada di URL
    if "download_mood" in query_params and query_params["download_mood"] == "true":
        # Hapus parameter dari URL agar tidak memicu unduhan berulang jika pengguna refresh
        # Ini akan membersihkan URL setelah unduhan dipicu
        new_query_params = query_params.to_dict()
        if "download_mood" in new_query_params:
            del new_query_params["download_mood"]
        st.query_params.clear() # Membersihkan semua query params
        st.query_params.update(**new_query_params) # Memuat kembali query params tanpa 'download_mood'
        
        # Kemudian, panggil JavaScript untuk unduhan
        components.html(
            f"""
            <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
            <script>
                // Pastikan html2canvas sudah dimuat sebelum mencoba menggunakannya
                if (typeof html2canvas === 'undefined') {{
                    console.error("html2canvas not loaded. Retrying...");
                    // Opsional: tunggu sebentar dan coba lagi, atau berikan pesan error ke user
                    setTimeout(downloadMoodAnalysis, 500); 
                }} else {{
                    downloadMoodAnalysis();
                }}

                function downloadMoodAnalysis() {{
                    const element = document.getElementById('mood-analysis-section');
                    if (!element) {{
                        console.error("Element with ID 'mood-analysis-section' not found for screenshot.");
                        return;
                    }}
                    html2canvas(element, {{ 
                        scale: 2, 
                        backgroundColor: 'rgba(10, 15, 30, 0.85)', 
                        useCORS: true, 
                        logging: false 
                    }}).then(canvas => {{
                        const link = document.createElement('a');
                        link.download = 'hasil_analisis_mood.png';
                        link.href = canvas.toDataURL('image/png');
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                        console.log("Screenshot download initiated.");
                    }}).catch(error => {{
                        console.error("Error during html2canvas capture:", error);
                    }});
                }}
            </script>
            """,
            height=0,
            width=0,
        )
        # st.toast("Download will start shortly!") # Opsional: beri feedback ke user

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