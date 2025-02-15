import streamlit as st

# page setup
about_page = st.Page(
    page="pages/about_me.py",
    title = "👩‍💻 About Me",
    
)

query_page = st.Page(
    page="pages/query.py",
    title = "💬 Chat", 
    default=True
   
)

# -- Navigation --

pg = st.navigation(
    {"Info": [about_page],
     "Project": [query_page]}
)

# st.logo("assests/bounce_insight_logo.png")

pg.run()




### 
import streamlit.components.v1 as components


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
    # Embed the particles.js HTML in the sidebar
with st.sidebar:
    components.html(particles_js, height=600, width=300, scrolling=False)