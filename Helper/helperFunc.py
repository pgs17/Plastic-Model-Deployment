from PIL import Image
import io
import pandas as pd
import numpy as np
import os
import json
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
    return return_image_array

# transform predict data in form of torch.tensor to numpy array   
def Transform_predict_to_Dataframe(predictions: list,label_dict:dict ={0:"Plastic"})-> pd.DataFrame:
    # df=pd.DataFrame()
    data=predictions[0].to("cpu").numpy().boxes
    df = pd.DataFrame(predictions[0].to("cpu").numpy().boxes.xyxy, columns=['xmin', 'ymin', 'xmax','ymax'])
    df["Confidence"] = data.conf
    print((data.cls).astype(int))
    # df["Labels"] = labels[(data.cls).astype(int)] # Maybe ?
    return df


# Perform model prediction
def get_model_predict( img: Image, model : YOLO, save: bool = False, imgsize : int = 640, conf: float= 0.31,flag: bool = False )->pd.DataFrame:
    predictions= model.predict( 
                        source=img, 
                        imgsz=imgsize,
                        conf=conf,
                        save=save,                       
                        )
    predictions= Transform_predict_to_Dataframe(predictions)
    if flag:
        predictions = predictions.to_json(orient='records')
    return predictions


# Count predictions
def count_predictions(predictions: pd.DataFrame) -> int:
     
    return len(json.loads(predictions))


# add bounding boxes to images by passing image and coordinates
def add_BoundingBoxes(image:Image,predict:pd.DataFrame)->Image:
    annotator=Annotator(np.array(image))

    predict=predict.sort_values(by =['xmin'],ascending=True) # to ensure bb are added from left to right

    for i, row in predict.iterrows():
        bounding_Box_coord=[row['xmin'],row['ymin'],row['xmax'],row['ymax']]
        # text=f"{row['name']}:{row['confidence']*100}%"
        annotator.box_label(bounding_Box_coord,color=(256,0,0))
         
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
    











