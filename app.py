import streamlit as st
import random

# --- Page Configuration ---
st.set_page_config(
    layout="wide",
    page_title="Cloud-Powered Recommendation System (UI Simulation)",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117; /* Dark background similar to the image */
        color: #E6E6E6; /* Light text color */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; /* A more modern font */
    }
    .stButton > button {
        background-color: #007bff; /* Primary blue button */
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 1.1em;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    /* Removed .stTabs specific CSS as tabs are no longer used for recommendations */
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #007bff; /* Headers in blue */
        border-bottom: 1px solid #2d384c; /* Subtle line under headers */
        padding-bottom: 5px;
        margin-bottom: 15px;
    }
    .stContainer {
        background-color: #1a222f; /* Darker container background */
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    /* Specific styles to mimic the glowing border look (limited effect in Streamlit) */
    .recommendation-box {
        border: 2px solid #007bff; /* Blue border */
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(0, 123, 255, 0.5); /* Glowing effect */
        background-color: #0d121c; /* Inner dark background */
        text-align: center;
    }
    /* Custom class for recommendation text font size */
    .recommendation-text p, .recommendation-text ul, .recommendation-text li {
        font-size: 15px !important; /* Set font size to 15px for all text within this class */
    }
    /* Make camera input smaller */
    .st-emotion-cache-1c7y2kl { /* This targets the outer div of st.camera_input in recent Streamlit versions */
        width: 50% !important;
        margin: 0 auto; /* Center the camera input */
        display: block; /* Ensure it takes up full width for centering to work */
    }
    .st-emotion-cache-1c7y2kl button { /* Targets the button specifically */
        width: 100% !important; /* Make the button fill the reduced width */
    }
    </style>
""", unsafe_allow_html=True)


col_header_left, col_header_right = st.columns([0.7, 0.3])

with col_header_right: # --- Header Section (Top Right like "Bakrieland" and "Powered By") ---
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/bakrieland_logo.png", width=150)
    st.markdown("""
        <p style='text-align: right; font-size: 0.8em; color: #888;'>
            POWERED BY <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/google_logo.png' width='50' style='vertical-align: middle; margin-left: 5px;'> <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/metrodata_logo.png' width='50' style='vertical-align: middle; margin-left: 5px;'>
        </p>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 2])

with col1: # --- Column 1: Property Recommendation ---
    st.markdown("<h2 style='text-align: center;'>PROPERTY RECOMMENDATION</h2>", unsafe_allow_html=True)
    st.markdown("<div class='recommendation-box'>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="KEMIRIPAN PURI WIDYAKARTA", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='recommendation-box'>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="BOGOR PUNCAK RESIDENCE", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


with col2: # --- Column 2: Holiday Recommendation ---
    st.markdown("<h2 style='text-align: center;'>HOLIDAY RECOMMENDATION</h2>", unsafe_allow_html=True)
    st.markdown("<div class='recommendation-box'>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="JUNGLE LAND", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='recommendation-box'>", unsafe_allow_html=True)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="RIVIERA OUTBOUND", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


with col3: # --- Column 3: Image Capture and Mood Analytic ---

    picture = st.camera_input("")

    if picture:
        # --- Simulated Mood Analysis Results ---
        simulated_moods = ["Happy", "Calm", "Energetic", "Thoughtful", "Brave", "Relaxed"]
        simulated_property = ["City apartment", "suburban chateau", "rural farmhouse", "beachfront villa", "mountain cabin"]
        simulated_holiday = ["Ocean Cruise","Beach Walk","Mountain Hiking","Forest Trekking","Mushroom Picking"]

        selected_mood = random.choice(simulated_moods)
        selected_property = random.choice(simulated_property)
        selected_holiday = random.choice(simulated_holiday)

        st.markdown("<h2 style='text-align: center;'>MOOD ANALYTIC</h2>", unsafe_allow_html=True)
        st.markdown(f"""
            <hr style="border-top: 1px dashed #2d384c;"/>
            <div class="recommendation-text">

                <p><strong>Analisa Mood:</strong></p>
                <ul>
                    <li>{selected_mood}</li>
                    <li>{selected_mood}</li>
                    <li>{selected_mood}</li>
                    <li>{selected_mood}</li>
                </ul>

                <p><strong>Property Recommendation:</strong>
                <ul>
                    <li>{selected_property}</li>
                    <li>{selected_property}</li>
                    <li>{selected_property}</li>
                </ul>

                <p><strong>Holiday Recommendation:</strong></p>
                <ul>
                    <li>{selected_holiday}</li>
                    <li>{selected_holiday}</li>
                    <li>{selected_holiday}</li>
                </ul>

            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <p style='text-align: center; padding-top: 20px; font-size: 1.1em; color: #aaa;'>
                📸 Awaiting image capture... Your mood analysis and recommendations will appear here.
            </p>
        """, unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey; font-size: 0.8em;'>&copy; 2025 Cloud-Powered Recommendation System UI. All rights reserved. (Simulated)</p>", unsafe_allow_html=True)
