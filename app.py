import streamlit as st
import requests
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

# Title
st.title("RAG System with Graph Generation")

# User Input
query = st.text_input("Ask a question:")

if st.button("Submit"):
    response = requests.get(f"http://127.0.0.1:8000/query?question={query}")

    if response.headers["Content-Type"] == "image/png":
        # Display the graph
        image = Image.open(BytesIO(response.content))
        st.image(image, caption="Generated Graph")
    else:
        # Display the response text
        st.write(response.json()["response"])