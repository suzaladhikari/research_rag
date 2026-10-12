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
        if response.status_code != 202:
            st.warning(f"Upload failed: {response.status_code}")
file_information = requests.get(f"{API_LINK}/documents")
for inf in file_information.json():
    c1, c2, c3 = st.columns([6,2,1])
    c1.write(inf["file_name"])
    c2.write(inf["status"])
    if c3.button("🗑️", key = f"del_{inf['file_id']}"):
        r = requests.delete(f"{API_LINK}/documents/{inf["file_id"]}")
        if r.ok:
            st.rerun()
        else:
            st.warning(f"Delete failed : {r.status_code}")


    
