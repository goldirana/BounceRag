
import streamlit as st
import os
import requests
import time
from math import ceil
from backend.src.utils import tempfile_cleaner
import streamlit.components.v1 as components

st.title("Query System")

def display_metadata(metadata_list):
    """
    Displays metadata in an expandable section.

    Args:
        metadata_list (list of dict): List of metadata dictionaries.
            Example: [{'filename': '2023_removed.pdf', 'page_number': '1'}, {'filename': '2023_removed.pdf', 'page_number': '1'}]
    """
    with st.expander("References"):
        st.markdown("**Metadata:**")
        # Using st.table for a neat tabular display
        st.table(metadata_list)
        

# FAST_API_URL = "http://0.0.0.0:5015"
FAST_API_URL = os.getenv("FAST_API_URL", "https://server-bnxb.onrender.com")
icons = {
    "user": "👤",  # Add user avatar
    "assistant": "frontend/static/ai.gif"
}

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    
    with st.chat_message(role, avatar=icons.get(role)):
        if isinstance(content, dict) and "images" in content:  # Handle images
            st.markdown(content["text"])
            st.subheader("Some Relevant Images")
            num_images = len(content["images"])
            cols_per_row = 3
            rows = ceil(num_images / cols_per_row)
            
            image_index = 0
            for _ in range(rows):
                cols = st.columns(cols_per_row)
                for col in cols:
                    if image_index < num_images:
                        img_url = f"{FAST_API_URL}{content['images'][image_index]}"
                        with col:
                            st.image(img_url, use_container_width=True)
                            
                    image_index += 1
        else:
            st.markdown(content)

# Chat input

query = st.chat_input("Message Insight Docs...")
if query == None:
    particles_js = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Particles.js Background</title>
  <style>
    /* Fullscreen fixed background for particles */
    #particles-js {
      position: fixed;
      width: 100vw;
      height: 100vh;
      top: 0;
      left: 0;
      z-index: -1; /* Send the animation behind other content */
    }
  </style>
</head>
<body>
  <div id="particles-js"></div>
  <script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
  <script>
    particlesJS("particles-js", {
      "particles": {
        "number": {
          "value": 300,
          "density": {
            "enable": true,
            "value_area": 800
          }
        },
        "color": {
          "value": "#ffffff"
        },
        "shape": {
          "type": "circle"
        },
        "opacity": {
          "value": 0.5
        },
        "size": {
          "value": 2,
          "random": true
        },
        "line_linked": {
          "enable": true,
          "distance": 100,
          "color": "#ffffff",
          "opacity": 0.22,
          "width": 1
        },
        "move": {
          "enable": true,
          "speed": 0.2,
          "out_mode": "out",
          "bounce": true
        }
      },
      "interactivity": {
        "detect_on": "canvas",
        "events": {
          "onhover": {
            "enable": true,
            "mode": "grab"
          },
          "onclick": {
            "enable": true,
            "mode": "repulse"
          },
          "resize": true
        },
        "modes": {
          "grab": {
            "distance": 100,
            "line_linked": {
              "opacity": 1
            }
          },
          "repulse": {
            "distance": 200,
            "duration": 0.4
          }
        }
      },
      "retina_detect": true
    });
  </script>
</body>
</html>
"""
    # Embed the particles.js HTML (adjust height as needed)
    components.html(particles_js, height=600,width=900 , scrolling=False)
if query:
    # Add user message to session state and display immediately
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user", avatar=icons["user"]):
        st.markdown(query)
    
    # Process the query and get response
    with st.chat_message("assistant", avatar=icons["assistant"]):
        assistant_text = st.empty()
        with st.spinner("Thinking..."):
            response = requests.post(f"{FAST_API_URL}/query", json={"question": query},
                                stream=True).json()
        
            text_response = response.get("response", "No response generated.")["content"]
            text_metadata = response.get("text_metadata")
            image_urls = response.get("images", [])
        
    # Stream the assistant's text response
        streamed_text = ""
        words = text_response.split()
        for i, word in enumerate(words):
            streamed_text = streamed_text + " " + word
            
            if i < len(words) - 1:
                assistant_text.markdown(streamed_text + "▌")
                time.sleep(0.1)
            else:
                assistant_text.markdown(streamed_text)

    # Display text metadata
        display_metadata(text_metadata)
    # Store response in session state
        if image_urls:
            st.session_state.messages.append({
                "role": "assistant", 
                "content": {
                    "text": streamed_text,
                    "images": image_urls
                }
            })
            st.subheader("Some Relevant Images")
            num_images = len(image_urls)
            cols_per_row = 3
            rows = ceil(num_images / cols_per_row)
            
            image_index = 0
            for _ in range(rows):
                cols = st.columns(cols_per_row)
                for col in cols:
                    if image_index < num_images:
                        img_url = f"{FAST_API_URL}{image_urls[image_index]}"
                        with col:
                            st.image(img_url, use_container_width=True)
                    image_index += 1
        else:
            st.session_state.messages.append({"role": "assistant", "content": streamed_text})