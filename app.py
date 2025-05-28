import streamlit as st
import random

# --- Page Configuration ---
st.set_page_config(
    layout="wide",
    page_title="Cloud-Powered Recommendation System (UI Simulation)",
    initial_sidebar_state="collapsed"
)

# --- Inject custom CSS for a darker theme and some visual resemblance ---
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
    .st-emotion-cache-1c7y2kl { /* This targets the outer div of st.camera_input */
        width: 50% !important;
        margin: 0 auto; /* Center the camera input */
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section (Top Right like "Bakrieland" and "Powered By") ---
col_header_left, col_header_right = st.columns([0.7, 0.3])
with col_header_right:
    # Using images from your GitHub repository
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/bakrieland_logo.png", width=150)
    st.markdown("""
        <p style='text-align: right; font-size: 0.8em; color: #888;'>
            POWERED BY <img src='https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/google_logo.png' width='50' style='vertical-align: middle; margin-left: 5px;'>
        </p>
    """, unsafe_allow_html=True)

st.markdown("---") # Separator

# --- Main Layout: Three Columns ---
col1, col2, col3 = st.columns([1, 1, 2]) # Adjust ratios as needed

# --- Column 1: Property Recommendation ---
with col1:
    st.markdown("<h2 style='text-align: center;'>PROPERTY RECOMMENDATION</h2>", unsafe_allow_html=True)
    st.markdown("<div class='recommendation-box'>", unsafe_allow_html=True)
    # Using property_image.jpeg from your GitHub repository
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="KEMIRIPAN PURI WIDYAKARTA", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='recommendation-box'>", unsafe_allow_html=True)
    # Using property_image.jpeg from your GitHub repository (repeated for second property)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/property_image.jpeg", caption="BOGOR PUNCAK RESIDENCE", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Column 2: Holiday Recommendation ---
with col2:
    st.markdown("<h2 style='text-align: center;'>HOLIDAY RECOMMENDATION</h2>", unsafe_allow_html=True)
    st.markdown("<div class='recommendation-box'>", unsafe_allow_html=True)
    # Using themepark_image.jpg from your GitHub repository
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="JUNGLE LAND", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='recommendation-box'>", unsafe_allow_html=True)
    # Using themepark_image.jpg from your GitHub repository (repeated for second themepark)
    st.image("https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/themepark_image.jpg", caption="RIVIERA OUTBOUND", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- Column 3: Image Capture and Mood Analytic ---
with col3:
    st.markdown("<h2 style='text-align: center;'>MOOD ANALYTIC</h2>", unsafe_allow_html=True)

    # --- Image Capture and Display ---
    st.subheader("Capture Your Mood!")
    st.markdown("<p style='font-size:0.9em; color:#bbb;'>Use your camera to take a picture for mood analysis simulation.</p>", unsafe_allow_html=True)
    # The label for camera_input is set to an empty string to remove the default button text
    picture = st.camera_input("")

    if picture:
        # --- Simulated Mood Analysis Results ---
        simulated_moods = ["Happy", "Calm", "Energetic", "Thoughtful", "Brave", "Relaxed"]
        selected_mood = random.choice(simulated_moods) # Pick a random mood for simulation

        # Combined Mood Analysis, Property, and Holiday Recommendation into a single block
        st.markdown(f"""
            <hr style="border-top: 1px dashed #2d384c;"/>
            <div class="recommendation-text">
                <p><strong>Mood Analysis:</strong> Based on a simulated analysis, your expression suggests a **{selected_mood}** mood. This typically correlates with someone who is:</p>
                <ul>
                    <li>Outlook: A generally positive and engaged disposition.</li>
                    <li>Energy Level: Moderate to high, ready for engagement.</li>
                    <li>Personality Traits: May include adaptability, curiosity, and a drive for personal fulfillment.</li>
                    <li>Core Feeling: A sense of well-being and openness.</li>
                </ul>

                <p><strong>Property Recommendation:</strong> For your simulated **{selected_mood}** mood, a recommended property might be:</p>
                <ul>
                    <li>Type: Placeholder Modern Villa / Green Residence</li>
                    <li>Description: This property is envisioned for individuals seeking a blend of comfort, modern aesthetics, and serene environments. It often features spacious interiors, smart home technologies, and access to community green spaces or nature reserves.</li>
                    <li>Key Features: Large windows for natural light, open-plan living, communal recreation areas, and proximity to wellness facilities.</li>
                </ul>

                <p><strong>Holiday Recommendation:</strong> For your simulated **{selected_mood}** mood, a recommended holiday might be:</p>
                <ul>
                    <li>Type: Placeholder Nature Escape / Urban Exploration</li>
                    <li>Description: An experience designed to refresh your senses and stimulate your interests, whether through tranquil natural beauty or the vibrant energy of a bustling city. Activities could range from leisurely hikes to cultural tours.</li>
                    <li>Key Activities: Hiking trails, local culinary experiences, historical site visits, or relaxing spa treatments.</li>
                </ul>
                <p style='font-size:0.8em; color:#888;'><i>(All recommendations are simulated and would be dynamically generated by a real system.)</i></p>
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
