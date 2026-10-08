import streamlit as st
from pydantic import BaseModel, Field
st.header("Ask Questions and Get Information about your documents")

## Creating the user interface 
min_words = 5
max_words = 1000
text = text = st.text_area(f"Enter text (between {min_words} and {max_words} words):",
    placeholder="Type your sentence here...",)
class AskQuestion(BaseModel):
    question: str = Field()

