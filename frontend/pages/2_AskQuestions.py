import streamlit as st
from pydantic import BaseModel, Field
import random 
from sentence_transformers import SentenceTransformer 
from backend.app.worker import chunk_text, vectorize_chunks
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
        st.session_state.messages.append({"role": "user", "message": question})

        answer = random.random()
        st.session_state.messages.append({"role": "SentinelRAG", "message": answer})
        st.rerun() ## To keep on rerunning

if st.button("Clear chat"):
    st.session_state.messages = []
## Dispalying the text: 
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['message'])

class AskQuestion(BaseModel): ## This is the base model
    question: str = Field(lt = min_words, gt = max_words)

for message in st.session_state.messages:
    chunks = chunk_text(AskQuestion(message['message'])) ## Validating if it matches the requirements
    response = requests.post(f"{API_LINK}/posting_question_vector", json = {"question_chunk": chunks})
    



    ### Converting question into the chunks 


