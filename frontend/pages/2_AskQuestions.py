import streamlit as st
import requests 
import os 
from dotenv import load_dotenv

## FastAPI LINK
load_dotenv()
API_LINK = os.getenv("API_URL")
print(API_LINK)

st.header("Ask Questions and Get Information about your documents")
## Creating the user interface 
min_words = 5
max_words = 1000


if "messages" not in st.session_state:
    st.session_state.messages = [] ## Creating an empty dict 

### Setting up space for the users 
question = st.text_area("Please write your quesiton")
if st.button("Send"):
    total_words = question.split()

    if not min_words <= len(total_words) <= max_words: 
        st.warning(f"Please make sure that the question is between {min_words} to {max_words} words")
    else:
        response = requests.post(f"{API_LINK}/posting_question_vector", json = {"question": question})
        st.session_state.messages.append({"role": "user", "message": question})
        st.session_state.messages.append({"role": "assistant", "message": response.json()['embedding']})
        st.rerun() ## To keep on rerunning

if st.button("Clear chat"):
    st.session_state.messages = []
## Dispalying the text: 
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['message'])







