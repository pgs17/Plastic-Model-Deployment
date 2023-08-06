
FROM python:3.11-slim


WORKDIR /Detect_API


COPY ./requirements.txt /Detect_API/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /Detect_API/requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y


  
COPY . /Detect_API

 
WORKDIR /Detect_API
EXPOSE 8000

 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT ["streamlit", "run", "Stream_lit.py", "--server.port=8501", "--server.address=0.0.0.0"]
 