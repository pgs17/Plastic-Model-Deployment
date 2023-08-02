import streamlit as st

st.set_page_config(page_title="Plastic Detector")
st.title("Clean Water Pollution")

image=st.file_uploader("Upload the image in jpg or jpeg",type=['jpg','jpeg'])
video=st.file_uploader("Upload the video in mp4 format",type=['mp4'])
