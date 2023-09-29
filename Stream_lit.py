import streamlit as st
import requests
import  io
from PIL import Image
import cv2
import phonenumbers
from pathlib import Path
import phonenumbers
from phonenumbers import geocoder
import math
import PIL.ExifTags
from geopy.geocoders import Nominatim
import pandas
from Helper.helperFunc import get_model_predict

url=" http://192.168.29.213:8501"



def main():

  st.set_page_config(page_title="Plastic Detector")
  st.title(" 🌊Detect Plastics and Improve Marine Life 🐠🦈 ") 

  img=st.file_uploader("Upload the image in jpg or jpeg for Detection",type=['jpg','jpeg'])
  number=st.text_input("Enter Your Phone Number With Country Code")
  # video=st.file_uploader("Upload the video in mp4 format",type=['mp4'])



  if img is not None:
    # st.image(Image.open(img),caption="Uploaded",use_column_width=True)
    if st.button("perform prediction"):
      detect_plastic( Image.open(img),number)
    else:
     st.image(Image.open(img),caption="Uploaded",use_column_width=True)

def geo(img):

    exif={PIL.ExifTags.TAGS[k]:v
        for k,v in img._getexif().items()
        if k in PIL.ExifTags.TAGS
      
        }
    n=exif['GPSInfo'][2]
    e=exif['GPSInfo'][4]
    ltd=(float)((((n[0]*60)+n[1])*60)+n[2])/60/60
    lng=(float)((((e[0]*60)+e[1])*60)+e[2])/60/60
    return ltd,lng

def live(number):
    divided=phonenumbers.parse(number)  
    if(phonenumbers.is_valid_number(divided)):
      location=geocoder.description_for_number(divided,"en")
      geolocator=Nominatim(user_agent="geoapiExercises")
      locate=geocoder.description_for_number(divided,'en')
      location=geolocator.geocode(locate)
      lat=location.latitude
      lng=location.longitude
      return 1,lat,lng
    else:
       return 0,0,0
       
 

def dist(ltd1,lng1,ltd2,lng2):
    R = 6371;
    p1 = ltd1 * math.pi/180;
    p2 = ltd2 * math.pi/180;
    dp = (ltd2-ltd1) * math.pi/180;
    dl = (lng2-lng1) * math.pi/180;

    a = math.sin(dp/2) * math.sin(dp/2) +math.cos(p1) * math.cos(p2) *math.sin(dl/2) * math.sin(dl/2);
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a));

    d = R * c;
    return d

def detect_plastic(image:Image,numb):
  # api_img="http://fastapi:8000/predict_to_image"
  api_img="http://localhost:6942/predict_save_image"
  image_byte=io.BytesIO()
  image.save(image_byte,format="JPEG")
  image_byte=image_byte.getvalue()
   
  lt1,ln1=geo(image)
    
  v,lt2,ln2=live(numb)
  if(v):
      distance=dist(lt1,ln1,lt2,ln2)
  else:
      st.warning("Enter a valid Phone Number")

  response=requests.post(api_img,files={"file":image_byte})
  if response.status_code==200 and v:
     st.image(Image.open(io.BytesIO(response.content)),caption=f"Detected at a distance of {distance} km",use_column_width=True)

  else:
     st.error("Error Detecting Objects")  




if __name__=="__main__":
  main()
