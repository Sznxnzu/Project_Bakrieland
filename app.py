import streamlit as st
from PIL import Image
import io

# Initialize with a default image only once
if "display_image" not in st.session_state:
    st.session_state.display_image = "https://via.placeholder.com/300?text=Initial+Image"

# Camera input
camera_picture = st.camera_input("Take a picture")

# If camera input is available, update the displayed image
if camera_picture is not None:
    st.session_state.display_image = camera_picture.getvalue()

# Display the current image (whether default or from camera)
if isinstance(st.session_state.display_image, bytes):
    st.image(st.session_state.display_image, caption="From Camera", use_column_width=True)
else:
    st.image(st.session_state.display_image, caption="Initial Image", use_column_width=True)
