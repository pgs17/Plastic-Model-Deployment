from PIL import Image
import io
import pandas as pd
import numpy as np

from typing import Optional

from ultralytics import YOLO
from ultralytics.yolo.utils.plotting import Annotator, colors

# Binary Bytes will be passed and we will get an Image Back
def get_Images_from_Bytes(binary_image:bytes)->Image:
    input_image=Image.open(io.BytesIO(binary_image)).convert("RGB")
    return input_image
     


# images will be passed and we will get the bytes back
def get_bytes_from_Images(image:Image)-> bytes:
    return_image=io.BytesIO()
    image.SAVE(return_image,format="JPEG",quality=86)
    return_image.seek(0) 
    return return_image

# transform predict data in form of torch.tensor to numpy array   
def Transform_predict_to_Dataframe(predictions: list,label_dict:dict ={0:"Plastic"})-> pd.DataFrame:
    df=pd.DataFrame()
    data=predictions[0].to("cpu").numpy.boxes
    df['xmin','ymin','xmax','ymax']=data.xyxy
    df['confidence']=data.conf
    # df['Class']=label_dict[(data.cls).astype(int)]
    return df





