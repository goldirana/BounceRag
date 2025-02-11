import streamlit as st
import os
from frontend.src.services import api
import sys

st.title("RAG System")

query = st.text_input("Ask a question:")
if st.button("Submit"):
    response = api.hello_world(query)
    st.write(response)

x = st.text_input("asdfad")
if st.button("test"):
    if x == "3":
        st.write("correct")
    else:
        st.write("wrong")
    