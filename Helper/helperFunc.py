from PIL import Image
import io
import pandas as pd
import numpy as np
import os

from typing import Optional

from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
# Annotator allows us to draw bounding boxes on images 

model=YOLO("Model2(Large).pt")

# Binary Bytes will be passed and we will get an Image Back
def get_Images_from_Bytes(binary_image:bytes)->Image:
    input_image=Image.open(io.BytesIO(binary_image)).convert("RGB")
    return input_image
     


# images will be passed and we will get the bytes back
def get_bytes_from_Images(image:Image)-> bytes:
    return_image_array=io.BytesIO()
    image.save(return_image_array,format="JPEG",quality=86)
    return_image_array.seek(0) 
    return return_image

# transform predict data in form of torch.tensor to numpy array   
def Transform_predict_to_Dataframe(predictions: list,label_dict:dict ={0:"Plastic"})-> pd.DataFrame:
    df=pd.DataFrame()
    data=predictions[0].to("cpu").numpy.boxes
    df['xmin','ymin','xmax','ymax']=data.xyxy
    df['confidence']=data.conf
    df['Class']=label_dict[(data.cls).astype(int)]
    return df


# Perform model prediction
def get_model_predict(model: YOLO , input_image: Image, save: bool = False, image_size: int = 640, conf: float = 0.41)->pd.DataFrame:
    predictions= model.predict(imgsz=image_size, 
                        source=input_image, 
                        conf=conf,
                        save=save,                       
                        )
    predictions= Transform_predict_to_Dataframe(predictions)
    
    return predictions

# add bounding boxes to images by passing image and coordinates
def add_BoundingBoxes(image:Image,predict:pd.DataFrame)->Image:
    annotator=Annotator(np.array(image))

    predict=predict.sort_values(by =predict['xmin'],ascending=True) # to ensure bb are added from left to right

    for i, row in predict.iterrows():
        bounding_Box_coord=[row['xmin'],row['ymin'],row['xmax'],row['ymax']]
        text=f"{row['name']}:{row['confidence']*100}%"
        annotator.box_label(bounding_Box_coord,text,color=colors(row['Class'],True))
         
         # converting the annnotated image to pIl image
    return Image.fromarray(annotator.result())

# save image along with the confidence values
def save_image(file_name:str,image:Image,prediction:pd.DataFrame,folder_name:str="Prediction")->None:
    folder_path=os.path.join(folder_name,file_name.split(".")[0])
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    image.save(os.path.join(folder_path,f"{file_name}_predicted.jpg"))

    with open(os.path.join(folder_path,f"{file_name}_predicted.txt"),"w") as file:
        file.write(prediction.to_string())    
    











