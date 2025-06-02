
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Bakrieland Mood Analytic", initial_sidebar_state="collapsed")

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
    }
    ::-webkit-scrollbar {
        display: none;
    }
.stApp {
    background-image: url("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/wallpaper_2.png");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    font-family: 'Segoe UI', sans-serif;
    color: white;
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
    font-size: 18px;
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
.mood-box {
    border: 2px solid #00f0ff;
    background-color: rgba(10, 15, 30, 0.85);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 0 0 20px #00f0ff;
    font-size: 8px;
    margin-top: 10px;
}
div[data-testid="stCameraInput"] > div {
    aspect-ratio: 4 / 5;
    width: 60% !important;
    height: auto !important;
    margin: 0;
    border-radius: 20px;
    overflow: hidden;
    background-color: rgba(0,0,0,0.1);
}
div[data-testid="stCameraInput"] video,
div[data-testid="stCameraInput"] img {
    object-fit: cover;
    width: 100%;
    height: 100%;
    border-radius: 20px;
}
div[data-testid="stCameraInput"] button[aria-label="Clear photo"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# HEADER
col_header_left, col_header_right = st.columns([0.8, 0.2])
with col_header_right:
    col_00, col_01 = st.columns([0.5, 0.5])
    with col_00:
        st.markdown("""
        <div style='display: flex; align-items: flex-end; height: 100%; justify-content: flex-start;'>
            <p style='font-size: 0.8em; color:#aaa; margin: 0;'>POWERED BY</p>
        </div>
        """, unsafe_allow_html=True)

    with col_01:
        st.markdown("""
        <div style='text-align: right;'>
            <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/bakrieland_logo.png' width='120' style='margin: 5px;'>
            <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/google_logo.png' width='50' style='margin: 5px;'>
            <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/metrodata_logo.png' width='50' style='margin: 5px;'>
        </div>
        """, unsafe_allow_html=True)

# MAIN 3-COLUMN LAYOUT
col1, col2, col3 = st.columns([1, 1, 1.4])

with col1:
    st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="portrait-box">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="KAHURIPAN NIRWANA", use_container_width=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="BOGOR NIRWANA RESIDENCE", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
    st.markdown('<div class="portrait-box">', unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="JUNGLE SEA", use_container_width=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="RIVERA OUTBOND", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="header-box">MOOD ANALYTIC</div>', unsafe_allow_html=True)
    cam_col, robot_col = st.columns([1.2, 1])

    with cam_col:
        picture = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed")
        if picture:
            st.image(picture, width=200)
            st.markdown("""
            <div class="mood-box">
                <p><strong>Analisa Mood:</strong></p>
                <ul>
                    <li>Percaya Diri: Terlihat dari sorot matanya dan posisi wajahnya.</li>
                    <li>Elegan/Glamor: Penampilannya secara keseluruhan memberikan kesan ini.</li>
                    <li>Tenang/Terkontrol: Tidak ada tanda-tanda kegelisahan atau kekacauan.</li>
                </ul>
                <p><strong>Property:</strong></p>
                <ul>
                    <li>Apartemen Mewah di Pusat Kota</li>
                    <li>Hunian Klasik Modern</li>
                    <li>Villa Eksklusif Pemandangan Alam</li>
                </ul>
                <p><strong>Rekomendasi Liburan:</strong></p>
                <ul>
                    <li>Liburan Santai di Resort</li>
                    <li>Perjalanan Kuliner Kota</li>
                    <li>Kapal Pesiar Mewah</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

    with robot_col:
        st.markdown("### 🤖 Robot Interaktif")
        components.html(
            """
            <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>

            <model-viewer id="robot" 
                src="https://cdn.jsdelivr.net/gh/husnanali05/FP_Datmin@main/cute-robot-colored.glb"
                alt="Cute Robot Colored 3D"
                camera-controls 
                auto-rotate 
                autoplay
                style="width: 100%; height: 400px;"
                ar 
                shadow-intensity="1"
                environment-image="neutral"
                exposure="1"
                interaction-prompt="none">
            </model-viewer>

            <script>
              const robot = document.querySelector("#robot");
              robot.addEventListener("click", () => {
                robot.currentTime = 0;
                robot.play();
              });
            </script>
            """, height=420)
