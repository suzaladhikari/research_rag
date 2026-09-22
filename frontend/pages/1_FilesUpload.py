import streamlit as st 
import requests 
import os 
from dotenv import load_dotenv

### File uploader 

uploaded_file = st.file_uploader("Please upload the files in here", type = ["pdf", "txt", "json"], accept_multiple_files=True)

## API 
load_dotenv()
API_LINK = os.getenv("API_URL")
print(API_LINK)
if uploaded_file and st.button("Submit"):
    st.success("Successfully submitted")
