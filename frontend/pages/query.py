import streamlit as st
import os
import requests
import time
from math import ceil
st.title("Query System")

# FAST_API_URL = "http://localhost:8501"
FAST_API_URL = os.getenv("FAST_API_URL", "http://localhost:8501")
icons = {"assistant": "assests/xxx.svg"}
query = st.chat_input("Message Insight Docs...")
if "messages" not in st.session_state:
    st.session_state_messages = []
    
if query:
    st.session_state_messages.append({"role": "user", "content": query})
    
    with st.chat_message("user"):
        st.markdown(query)
        
    with st.chat_message("assistant", avatar=icons["assistant"]):
        assistant_text = st.empty()

        with st.spinner("Thinking..."):
            response = requests.post(f"{FAST_API_URL}/query", json={"question": query},
                                     stream=True).json()
        
        text_response = response.get("response", "No response generated.")["content"]
        # print("--"* 100)
        # print(text_response)
        image_urls = response.get("images", [])
        
        streamed_text = ""
        for word in text_response.split():
            streamed_text = streamed_text + " " + word
            assistant_text.markdown(streamed_text + "▌") 
            time.sleep(0.1)
        assistant_text.markdown(streamed_text)
        
        time.sleep(2)
        if image_urls:
            st.subheader("Some helpful images: icon")
            
            num_images = len(image_urls)
            cols_per_row = 3  # Adjust number of columns per row
            rows = ceil(num_images / cols_per_row)

            # Create grid structure
            image_index = 0
            for _ in range(rows):
                cols = st.columns(cols_per_row)  # Creates 3 columns in each row
                for col in cols:
                    if image_index < num_images:
                        img_url = f"{FAST_API_URL}{image_urls[image_index]}"
                        with col:
                            st.image(img_url, use_container_width=True)
                    image_index += 1
                        
with st.container():
    for message in st.session_state_messages:
        role = message["role"]
        content = message["content"]
        
        with st.chat_message(role):
            st.markdown(content)
