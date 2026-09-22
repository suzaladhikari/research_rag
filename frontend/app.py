### This will be the streamlit app 
import streamlit as st
import requests

st.set_page_config(
    page_title="SentinelRAG",
    page_icon="🛡️",
    layout="wide",
)

st.title("SentinelRAG")
st.caption("Corporate Security made more secure")

### Filling up the form 

with st.form("Login Form"):
    email = st.text_input("Work email")
    password = st.text_input("Password", type = 'password')
    submitted = st.form_submit_button("Sign in", use_container_width=True)