import streamlit as st
from pydantic import BaseModel, Field
import random 
st.header("Ask Questions and Get Information about your documents")
## Creating the user interface 
min_words = 5
max_words = 1000


if "messages" not in st.session_state:
    st.session_state.message = [] ## Creating an empty dict 

### Setting up space for the users 
if st.button("Send"):
    question = st.text_area("Please write your quesiton")
    total_words = question.split()

    if not min_words <= len(total_words) <= max_words: 
        print("Can you shorten your question please")
    else:
        st.session_state.messages.append({"role": "user", "messages": question})

        answer = random.random()
        st.session_state.message.append({"role": "SentinelRAG", "message": answer})
        st.rerun() ## To keep on rerunning

## Dispalying the text: 
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

class AskQuestion(BaseModel):
    question: str = Field()

