import streamlit as st
from PIL import Image
import io
import requests

# Initialize the image URL in session state
if "image_url" not in st.session_state:
    st.session_state.image_url = "https://via.placeholder.com/300?text=Initial+Image"

def update_image():
    # Update the image URL to a new one or generate a new image
    st.session_state.image_url = "https://via.placeholder.com/300?text=Updated+Image"

st.image(st.session_state.image_url)

if st.button("Update Image"):
    update_image()
