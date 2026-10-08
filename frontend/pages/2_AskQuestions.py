import streamlit as st
from pydantic import BaseModel, Field
import random 
st.header("Ask Questions and Get Information about your documents")
## Creating the user interface 
min_words = 5
max_words = 1000
### Creating a dictionary that stores the messages even though the browser is reran 
if "messages" not in st.sessison_state:
    st.session_state.message = [] ## Creating an empty dict 
class AskQuestion(BaseModel):
    question: str = Field()

