import streamlit as st 
import requests 
import os 
from dotenv import load_dotenv

### File uploader 

uploaded_files = st.file_uploader("Please upload the files in here", type = ["pdf", "txt", "json"], accept_multiple_files=True)

## API 
load_dotenv()
API_LINK = os.getenv("API_URL")
print(API_LINK)
if uploaded_files and st.button("Submit"):
    for uploaded_file in uploaded_files:
        response = requests.post(f'{API_LINK}/posting_router', files={"file": (uploaded_file.name, uploaded_file.getvalue())},)
        if response.status_code == 202:
            st.success("It has been posted")
            st.write(response.json()['content'])
        else: 
            st.warning(response.status_code)
            st.write(response.json())

    
