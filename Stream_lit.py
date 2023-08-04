import streamlit as st
import requests
import  io
from PIL import Image
import cv2


url=" http://192.168.29.213:8501"



def main():

  st.set_page_config(page_title="Plastic Detector")
  st.title(" Detect Plastics With Yolo Model ")

  img=st.file_uploader("Upload the image in jpg or jpeg",type=['jpg','jpeg'])
  # video=st.file_uploader("Upload the video in mp4 format",type=['mp4'])

  if img is not None:
    st.image(Image.open(img),caption="Uploaded",use_column_width=True)
    if st.button("perform prediction"):
      detect_plastic( Image.open(img))




def detect_plastic(image:Image):
   api_img="http://localhost:6942/predict_save_image"
   image_byte=io.BytesIO()
   image.save(image_byte,format="JPEG")
   image_byte=image_byte.getvalue()

   response=requests.post(api_img,files={"file":image_byte})
   if response.status_code==200:
     st.image(Image.open(io.BytesIO(response.content)),caption="Detected",use_column_width=True)

   else:
     st.error("Error Detecting Objects")  



if __name__=="__main__":
  main()
