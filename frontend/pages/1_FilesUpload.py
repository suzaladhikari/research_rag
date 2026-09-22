import streamlit as st 
import requests 


### File uploader 

uploaded_file = st.file_uploader("Please upload the files in here", type = ["pdf", "txt", "json"], accept_multiple_files=True)

if uploaded_file and st.button("Submit"):
    st.success("Successfully submitted")
