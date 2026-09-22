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