 # Stage 1: Build the FastAPI application
FROM python:3.11-slim AS fastapi_builder

WORKDIR /Detect_API

COPY ./requirements.txt /Detect_API/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /Detect_API

# Stage 2: Build the Streamlit application
FROM python:3.11-slim AS streamlit_builder

WORKDIR /Detect_API

COPY ./requirements.txt /Detect_API/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /Detect_API

# Final Stage: Create the production image
FROM python:3.11-slim

# Copy FastAPI files from the fastapi_builder stage
COPY --from=fastapi_builder /Detect_API /Detect_API

# Copy Streamlit files from the streamlit_builder stage
COPY --from=streamlit_builder /Detect_API /Detect_API

WORKDIR /Detect_API

# Install additional dependencies for Streamlit
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

EXPOSE 8000
EXPOSE 8501

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
ENTRYPOINT ["streamlit", "run", "Stream_lit.py", "--server.port", "8501", "--server.address", "0.0.0.0"]