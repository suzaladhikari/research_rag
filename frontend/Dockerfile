## This is for the streamlit 
FROM python:3.11-slim

WORKDIR /streamlit  #This is the working directory that will be used or kept the files in 

COPY frontend/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY frontend ./frontend

EXPOSE 8000 

CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]