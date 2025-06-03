import streamlit as st
import streamlit.components.v1 as components
import google.generativeai as genai
from PIL import Image
import io
import requests
import html

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
    font-size: 10px;
    margin-top: 10px;
    width: 100%;
    height: 40vh;
}
.mood-box p {
    margin-bottom: 0;
}
.mood-box ul {
    margin-top: 0;
    margin-bottom: 1em;
    padding-left: 20px;
}
div[data-testid="stCameraInput"] > div {
    aspect-ratio: 4 / 5;
    width: 60% !important;
    height: auto !important;
    margin: 0;
    border-radius: 20px;
    background-color: rgba(0, 0, 0, 0.1);
}
div[data-testid="stCameraInput"] button {
    display: inline-block !important;
    visibility: visible !important;
    position: relative !important;
    z-index: 10 !important;
}
div[data-testid="stCameraInput"] video,
div[data-testid="stCameraInput"] img {
    object-fit: cover;
    width: 100%;
    height: 100%;
    border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)

genai.configure(api_key= st.secrets["gemini_api"])
model = genai.GenerativeModel("gemini-1.5-flash-latest")

col_header_left, col_header_right = st.columns([0.85, 0.15])
with col_header_right:
    col_00, col_01 = st.columns([0.3, 0.7])
    with col_00:
        st.markdown("""
        <div style='display: flex; align-items: flex-end; height: 100%; justify-content: flex-start;'>
            <p style='font-size: 0.6em; color:#aaa; margin: 0;'>POWERED BY</p>
        </div>
        """, unsafe_allow_html=True)

    with col_01:
        st.markdown("""
        <div style='text-align: right;'>
            <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/bakrieland_logo.png' width='120' margin: 5px;'>
            <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/google_logo.png' width='50' style='margin: 5px;'>
            <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/metrodata_logo.png' width='50' style='margin: 5px;'>
        </div>
        """, unsafe_allow_html=True)

    components.html(
        """
        <script type="module" src="https://unpkg.com/@google/model-viewer/dist/model-viewer.min.js"></script>

        <model-viewer id="robot" 
            src="https://cdn.jsdelivr.net/gh/husnanali05/FP_Datmin@main/nerinho_-_mascote_da_neomind.glb"
            alt="Robot Nerinho 3D"
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
        """,
        height=420
    )
    st.markdown("""
          <div class="qr-box">
              <img src="https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/qr_logo.png" style="width:100%; border-radius: 8px;" />
          </div>
        """, unsafe_allow_html=True)

with col_header_left:
    col1, col2, col3 = st.columns([1, 1, 1.4])

    placeholder_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/other/placeholder.png"
    placeholder_caption = ""
    placeholder_analysis = ""

    if "image_states" not in st.session_state:
      st.session_state.image_states = [placeholder_url, placeholder_url, placeholder_url, placeholder_url]
    if "image_captions" not in st.session_state:
      st.session_state.image_captions = [placeholder_caption, placeholder_caption, placeholder_caption, placeholder_caption]
    if "image_analysis" not in st.session_state:
      st.session_state.image_analysis = [placeholder_analysis]
    if "has_rerun" not in st.session_state:
      st.session_state.has_rerun = False


    with col1:

        url_list_1 = []
        for url in st.session_state.image_states[:2]:
          url_list_1.append(url)
        cap_list_1 = []
        for captions in st.session_state.image_captions[:2]:
          cap_list_1.append(captions)

        st.markdown('<div class="header-box">PROPERTY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""
          <div class="portrait-box">
              <img src="{url_list_1[0]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
              <p style="text-align:center; margin-top: 5px; font-size: 0.9em; color: #ccc;">{cap_list_1[0]}</p>
              <img src="{url_list_1[1]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
              <p style="text-align:center; margin-top: 5px; font-size: 0.9em; color: #ccc;">{cap_list_1[1]}</p>
          </div>
        """, unsafe_allow_html=True)

    with col2:
        url_list_2 = []
        for url in st.session_state.image_states[2:]:
          url_list_2.append(url)
        cap_list_2 = []
        for captions in st.session_state.image_captions[2:]:
          cap_list_2.append(captions)

        st.markdown('<div class="header-box">HOLIDAY RECOMMENDATION</div>', unsafe_allow_html=True)
        st.markdown(f"""
          <div class="portrait-box">
              <img src="{url_list_2[0]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
              <p style="text-align:center; margin-top: 5px; font-size: 0.9em; color: #ccc;">{cap_list_2[0]}</p>
              <img src="{url_list_2[1]}" style="width:100%; height:200px; border-radius:8px; object-fit:cover;" />
              <p style="text-align:center; margin-top: 5px; font-size: 0.9em; color: #ccc;">{cap_list_2[1]}</p>
          </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("<p style='text-align: center; font-size:0.9em; color:#bbb;'></p>", unsafe_allow_html=True)
        user_input = st.camera_input("Ambil foto wajah Anda", label_visibility="collapsed")
        if user_input:
            image = Image.open(io.BytesIO(user_input.getvalue()))

            if image is not None:

              url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt.txt"
              response = requests.get(url)
              prompt = response.text
              response = model.generate_content([prompt, image])
              raw_output = response.text
              escaped_text = html.escape(response.text)

              url_json = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/prompt_json.txt"
              response_json = requests.get(url_json)
              prompt_json = response_json.text
              response_json = model.generate_content([prompt_json, raw_output])

              # st.write("**Gemini says:**", response_json.text)

              filenames = response_json.text.strip().split(",")
              midpoint = len(filenames) // 2
              first_filenames = filenames[:midpoint]
              second_filenames = filenames[midpoint:]

              imgpath_property_1 = f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{first_filenames[0].strip()}.jpg"
              imgpath_property_2 = f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/property/{first_filenames[1].strip()}.jpg"
              imgpath_holiday_1 = f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{second_filenames[0].strip()}.jpg"
              imgpath_holiday_2 = f"https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/holiday/{second_filenames[1].strip()}.jpg"

              imgcap_property_1 = first_filenames[0].strip()
              imgcap_property_2 = first_filenames[1].strip()
              imgcap_holiday_1 = second_filenames[0].strip()
              imgcap_holiday_2 = second_filenames[1].strip()

              updated_image_analysis = escaped_text

              updated_image_urls = [
                  imgpath_property_1,
                  imgpath_property_2,
                  imgpath_holiday_1,
                  imgpath_holiday_2
              ]

              updated_image_captions = [
                  imgcap_property_1,
                  imgcap_property_2,
                  imgcap_holiday_1,
                  imgcap_holiday_2
              ]

              st.session_state.image_states = updated_image_urls
              st.session_state.image_captions = updated_image_captions
              st.session_state.image_analysis = [updated_image_analysis]

              if not st.session_state.has_rerun:
                st.session_state.has_rerun = True
                st.rerun()
        
        analysis_list = []
        for analysis in st.session_state.image_analysis:
          analysis_list.append(analysis)
        st.markdown(f"""
          <div class="mood-box">
          <pre style="white-space: pre-wrap;">{analysis_list[0]}</pre>
          </div>
          """, unsafe_allow_html=True)
