import streamlit as st 
import requests 


### File uploader 

uploaded_file = st.file_uploader("Please upload the files in here", type = ["pdf", "txt", "json"], accept_multiple_files=True)
total_files = set(uploaded_file.name)
for each in total_files:
    st.write(total_files)

st.divider()
