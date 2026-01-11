import streamlit as st
from PIL import Image

st.set_page_config(layout="wide")

st.title('Image Converter')

# Create a file uploader component allowing the user to upload a file
uploaded_image = st.file_uploader('Upload image')

if uploaded_image is not None:
    # Open the user uploaded image with PIL
    img = Image.open(uploaded_image)

    # Convert the pillow image to grayscale
    gray_uploaded_img = img.convert('L')

    # Render the grayscale image on the webpage
    st.image(gray_uploaded_img, use_column_width=True)

with st.expander('Start Camera'):
    # Start the camera
    camera_image = st.camera_input('Camera')

if camera_image:
    # Create a pillow image instance
    img = Image.open(camera_image)

    # Convert the pillow image to grayscale
    gray_camera_img = img.convert('L')

    # Render the grayscale image on the webpage
    st.image(gray_camera_img, use_column_width=True)