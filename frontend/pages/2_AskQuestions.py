import streamlit as st
from pydantic import BaseModel, Field
import random 
st.header("Ask Questions and Get Information about your documents")
## Creating the user interface 
min_words = 5
max_words = 1000
users_texts = []
text = st.text_area(f"Enter text (between {min_words} and {max_words} words):",
    placeholder="Type your sentence here...",)

if st.button("Send"):
    if text:
        st.write(f"User: {text}")
        st.write(random.random())
class AskQuestion(BaseModel):
    question: str = Field()

