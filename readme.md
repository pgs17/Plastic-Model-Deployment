#Plastic-Model-Deployment

## Problem Statement
  Develop a reliable and efficient AI-based object detection model using drone images to detect plastic waste in rivers and demonstrate a feasible solution/system architecture for implementation, ultimately reducing the negative impact of plastic pollution on the environment and human health.
 

## Objective


This project aims to:

- detect plastic waste in rivers and help in reducing water pollution
- to give the location of river and alsom the distance from the user's currnt location where plastic is present and also latitude and longitude of plastic

## Proposed Solution

This project covers all aspects that need to be emphasised on to minimise the problem:
- plastic is detected
- location of river is given
- latitude and longitude of plastic is given
-distance between plastic and the device/concerned authorities is given

## Proposed TechStack
<ul>
<li>Python</li>
<li>Yolov8(for model training refer:ultralytics)</li>
<li>Streamlit(for web app)</li>
<li>FastAPI(for creating API endpoints)</li>
<li>Docker(For dockerising the entire content for hosting)</li>
<li>Cvat(For annotation purpose)</li>
</ul>


## Steps to Start our WebApp:
-First clone the repo
- Create a Virtual Environment and activate it
- pip install requirements.txt (basically fastapi ultralytics streamlit phonenumbers geopy PIL pathlib)
- Run *python startscript.py* to start the server and *streamlit run Stream_lit.py* to start the frontend


## To start server only:
- docker build -t yolo .
- docker run -p 8000:8000 yolo
- now we can go on local host 8000 and test the API
