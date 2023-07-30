from PIL import Image
import io
import pandas as pd
import numpy as np

from typing import Optional

from ultralytics import YOLO
# from ultralytics.yolo.utils.plotting import Annotator, colors

model=YOLO("Model2(Large).pt")

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


# Perform model prediction
def get_model_predict(model: YOLO , input_image: Image, save: bool = False, image_size: int = 1248, conf: float = 0.41, augment: bool = False)->pd.DataFrame:
    predictions= model.predict(imgsz=image_size, 
                        source=input_image, 
                        conf=conf,
                        save=save, 
                        augment=augment,
                        flipud= 0.0,
                        fliplr= 0.0,
                        mosaic = 0.0,)
    # flipud and fliplr and mosaic are augmentation parameters set to 00 to avoid augmentation on those params
    predictions= Transform_predict_to_Dataframe(predictions,model.model.names)
    # model.model.names will map the numeric values to their class labels
    return predictions


# does preddiction on sample image
def get_sample_model(input_image:Image)->pd.DataFrame:
    predict=get_model_predict(
        model=model,
        input_image=input_image,
        save=False,
        augment=False,
        conf=0.41,
        image_size=640
    )
    return predict







