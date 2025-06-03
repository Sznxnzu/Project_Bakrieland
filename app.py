import streamlit as st
from PIL import Image
import io
import requests

# Initialize the image URL in session state
if "image_url" not in st.session_state:
    st.session_state.image_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/qr_logo.png"

def update_image():
    # Update the image URL to a new one or generate a new image
    st.session_state.image_url = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/metrodata_logo.png"

st.image(st.session_state.image_url)

if st.button("Update Image"):
    update_image()
