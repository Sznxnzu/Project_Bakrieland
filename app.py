import streamlit as st
import random

# --- Page Configuration ---
st.set_page_config(
    layout="wide",
    page_title="Bakrieland Project",
    initial_sidebar_state="collapsed"
)

# --- Inject custom CSS ---
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/wallpaper.png");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-color: #0E1117;
        color: #E6E6E6;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton > button { background-color: #007bff; color: white; border-radius: 8px; padding: 10px 20px; font-size: 1.1em; transition: background-color 0.3s ease; }
    .stButton > button:hover { background-color: #0056b3; }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #007bff; border-bottom: 1px solid #2d384c; padding-bottom: 5px; margin-bottom: 15px; }

    .header-with-bg {
        background-image: url('https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/header_bg.png');
        background-size: cover;
        background-position: center;
        padding: 0px 0px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 0px;
        border: 1px solid rgba(0, 123, 255, 0.4);
        color: #ffffff;
    }

    .stContainer { background-color: rgba(26, 34, 47, 0.9); padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    .recommendation-box {
        border: 2px solid #007bff;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 123, 255, 0.5);
        background-color: rgba(13, 18, 28, 0.9);
        text-align: center;
    }
    .recommendation-text p, .recommendation-text ul, .recommendation-text li { font-size: 15px !important; }

    div[data-testid="stCameraInput"] > div {
        width: 50% !important;
        height: 50% !important; 
        margin: 0; 
        float: left;
        background-color: rgba(14, 17, 23, 0.9);
        overflow: hidden;
        border-radius: 8px;
    }
    div[data-testid="stCameraInput"] video,
    div[data-testid="stCameraInput"] img {
        width: 100% !important;
        height: 100% !important;
        object-fit: cover;
        border-radius: 8px;
    }
    div[data-testid="stCameraInput"] button {
        width: 100% !important;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

col_header_left, col_header_right = st.columns([0.9, 0.1])

with col_header_right:
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/bakrieland_logo.png", width=150)
    st.markdown(
        "<p style='text-align: right; font-size: 0.8em; color: #888;'>"
        "POWERED BY "
        "<img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/google_logo.png' width='80' style='vertical-align: middle; margin-left: 5px;'>"
        "<img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/metrodata_logo.png' width='50' style='vertical-align: middle; margin-left: 5px;'>"
        "</p>",
        unsafe_allow_html=True
    )

with col_header_left:
  
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        st.markdown("""
            <div class="header-with-bg">
                <h2 style='text-align: center; margin-bottom: 0;'>PROPERTY RECOMMENDATION</h2>
            </div>
        """, unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="KEMIRIPAN PURI WIDYAKARTA", use_container_width=True)
        st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="BOGOR PUNCAK RESIDENCE", use_container_width=True)

    with col2:
        st.markdown("""
            <div class="header-with-bg">
                <h2 style='text-align: center; margin-bottom: 0;'>HOLIDAY RECOMMENDATION</h2>
            </div>
        """, unsafe_allow_html=True)
        st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="JUNGLE LAND", use_container_width=True)
        st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="RIVIERA OUTBOUND", use_container_width=True)

    with col3:
        picture = st.camera_input("")
        if picture:
            simulated_moods = ["Happy", "Calm", "Energetic", "Thoughtful", "Brave", "Relaxed"]
            simulated_property_options = ["City apartment", "Suburban chateau", "Rural farmhouse", "Beachfront villa", "Mountain cabin"]
            simulated_holiday_options = ["Ocean Cruise", "Beach Walk", "Mountain Hiking", "Forest Trekking", "Mushroom Picking"]

            selected_mood = random.choice(simulated_moods)
            selected_property = random.choice(simulated_property_options)
            selected_holiday = random.choice(simulated_holiday_options)

            html_content = (
                "<div class='recommendation-text'>"
                "<p><strong>Analisa Mood:</strong></p>"
                f"<ul><li>{selected_mood}</li><li>{selected_mood}</li><li>{selected_mood}</li><li>{selected_mood}</li></ul>"
                "<p><strong>Property Recommendation:</strong></p>"
                f"<ul><li>{selected_property}</li><li>{selected_property}</li><li>{selected_property}</li></ul>"
                "<p><strong>Holiday Recommendation:</strong></p>"
                f"<ul><li>{selected_holiday}</li><li>{selected_holiday}</li><li>{selected_holiday}</li></ul>"
                "</div>"
            )
            st.markdown(html_content, unsafe_allow_html=True)
        else:
            st.markdown(
                "<p style='text-align: left; padding-top: 20px; font-size: 1.1em; color: #aaa;'>"
                "Awaiting image capture..."
                "</p>",
                unsafe_allow_html=True
            )
