import streamlit as st
from PIL import Image
import io

# Initialize with a default image only once
if "display_image" not in st.session_state:
    st.session_state.display_image = "https://raw.githubusercontent.com/Sznxnzu/Project_Bakrieland/main/resources/logo/qr_logo.png"

# Show current image
st.image(st.session_state.display_image, caption="Current Image", use_column_width=True)

# Take picture from camera
camera_picture = st.camera_input("Take a picture")

# Button to update the displayed image
if st.button("Use This Photo") and camera_picture is not None:
    # Convert camera input (bytes) into a PIL image (or just store bytes)
    image_bytes = camera_picture.getvalue()
    st.session_state.display_image = image_bytes  # You can also save image to disk or cloud here

# If the display_image is bytes (camera input), show it
if isinstance(st.session_state.display_image, bytes):
    st.image(st.session_state.display_image, caption="Updated from Camera", use_column_width=True)
