import streamlit as st
from pydantic import BaseModel, Field
import random 
st.header("Ask Questions and Get Information about your documents")
## Creating the user interface 
min_words = 5
max_words = 1000

### Setting up space for the users 
question = st.text_area("Please write your quesiton")
total_words = question.split()
if min_words < len(total_words) or len(total_words) > max_words: 
    print("Can you shorten your question please")
st.session_state.messages.append({"role": "user", "messages": question})
### Creating a dictionary that stores the messages even though the browser is reran 

if "messages" not in st.session_state:
    st.session_state.message = [] ## Creating an empty dict 

### Displaying the messages: 

class AskQuestion(BaseModel):
    question: str = Field()

