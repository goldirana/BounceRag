import streamlit as st
import os
from PIL import Image
import markdown

from frontend.components.contact import contact_form
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    body {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(135deg, #f0f4f8, #d9e2ec);
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# -------------------------------
# CUSTOM CSS FOR CONTACT ME BUTTON & EXPANDER HEADER
# -------------------------------
st.markdown(
    """
    <style>
    /* Styling for the Contact Me button with a white (colorless) background and 3D effect */
    div.stButton > button {
        background-color: #ffffff !important;
        border: 1px solid #eaeaea !important;
        color: #000000 !important;
        border-radius: 8px;
        padding: 0.5rem 1rem !important;
        font-weight: 600;
        box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 5px 5px 12px rgba(0, 0, 0, 0.2);
    }
    
    /* Styling for the expander header (clickable outer box) with a white background and 3D effect */
    div.stExpander > button {
        background-color: #ffffff !important;
        border: 1px solid #eaeaea !important;
        color: #000000 !important;
        border-radius: 8px;
        padding: 0.5rem 1rem !important;
        font-weight: 600;
        box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div.stExpander > button:hover {
        transform: translateY(-2px);
        box-shadow: 5px 5px 12px rgba(0, 0, 0, 0.2);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.dialog("Contact Me")
def show_contact_form():
    contact_form()

# Get the directory where the current script is located

image_path = "frontend/static/profile.png"

# Layout: use columns to place image and text side by side
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

# Left Column: Profile Image
with col1:
    try:
        profile_image = Image.open(image_path)
        st.image(profile_image, width=230)
    except Exception as e:
        st.error("Profile image not found. Please ensure 'profile.jpg.png' exists in the same directory.")

# Right Column: About Me Text and Social Links
with col2:
    st.markdown(
    """
    <div class="hero" style="text-align: center; margin-top: 1rem; margin-bottom: 2rem;">
       <h1 style="font-size: 3rem; margin-bottom: 0; animation: fadeIn 1s ease-in-out;">Rajesh Goldy</h1>
       <h3 style="margin: 0; animation: fadeIn 1.5s ease-in-out;">Data Scientist, Based in Ireland</h3>
    </div>
    <style>
       @keyframes fadeIn {
           from { opacity: 0; }
           to { opacity: 1; }
       }
    </style>
    """,
    unsafe_allow_html=True,
    )
    
    # Social Links Section with improved icon UI (keeping the previous bright yellow style)
    st.markdown(
        """
        <div style="display: flex; gap: 1rem; align-items: center; margin-bottom: 1.5rem;">
            <a href="https://www.datascienceportfol.io/rajeshgoldy" target="_blank">
                <img class="icon" src="https://img.icons8.com/fluency/48/000000/domain.png" alt="Portfolio">
            </a>
            <a href="https://github.com/goldirana" target="_blank">
                <img class="icon" src="https://img.icons8.com/fluency/48/000000/github.png" alt="GitHub">
            </a>
            <a href="https://www.linkedin.com/in/rajeshgoldy" target="_blank">
                <img class="icon" src="https://img.icons8.com/fluency/48/000000/linkedin.png" alt="LinkedIn">
            </a>
        </div>
        <style>
            .icon {
                height: 30px;
                border-radius: 8px;
                box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.3);
                transition: transform 0.2s, box-shadow 0.2s, background-color 0.2s;
                background-color: #FFD93D; /* previous bright yellow background */
                padding: 5px;
            }
            .icon:hover {
                transform: translateY(-2px);
                box-shadow: 5px 5px 12px rgba(0, 0, 0, 0.4);
                background-color: #FFC107; /* slightly different bright color on hover */
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    if st.button("📧 Contact Me"):
        show_contact_form()
    
# --- EXPERIENCE SECTION ---
st.write("\n")
st.subheader("Experience", anchor=False)
st.write("Click on each section below to view detailed experience:")

def expander_experience(title, content):
    with st.expander(title):
        # Convert the markdown content to HTML and wrap it in a styled div
        # The inner content remains with its previous color scheme.
        html_content = markdown.markdown(content)
        styled_html = (
            "<div style='background-color:#1a1a1a; color: #ffffff; padding:1rem; border-radius:8px; border:1px solid #444444;'>"
            + html_content +
            "</div>"
        )
        st.markdown(styled_html, unsafe_allow_html=True)

# Experience Details

expander_experience(
    "Sept 2021 – March 2023: Data Analyst onsite, Google, India",
    """
**Impact-driven Data Analyst** who designed and implemented data management strategies and hypothesis experiments.  
- Drove a **6% increase** in conversion rates for financial products through insightful user behavior analysis.  
- Played a key role in optimizing cost efficiency and resource allocation, resulting in a **$1M revenue impact**.  
- Proactively identified transactional anomalies to improve financial fraud accuracy and mitigate risks.  
- Developed automated tools for A/B testing, ensuring streamlined processes and enhanced data integrity.
    """
)

expander_experience(
    "April 2021 – Sep 2021: Data Scientist at NIIT Pvt. Ltd, India",
    """
**Expert Mentor & Data Scientist** specializing in leveraging statistical methodologies to optimize product performance.  
- Achieved a **10% improvement** in course completion rates.  
- Built machine learning models to reduce student churn, enhancing retention and driving revenue growth.  
- Conducted high-impact workshops with an **87% satisfaction rate**.  
- Translated complex analyses into actionable insights for stakeholders.
    """
)

expander_experience(
    "Aug 2020 – Feb 2021: Executive onsite @ IBM",
    """
**Skilled Trainer & Strategist** focused on delivering exceptional corporate training sessions in data science and machine learning.  
- Designed bespoke training programs tailored to client needs.  
- Cultivated strong client relationships by providing timely and effective training solutions.  
- Leveraged industry insights to align educational offerings with emerging trends, positioning the organization for long-term success.
    """
)

expander_experience(
    "Jan 2020 – Jun 2020: Data Scientist at WhiteSquare Technologies, India",
    """
**Innovative Data Scientist** specializing in cryptocurrency analysis and algorithmic trading systems.  
- Fetched and transformed Bitcoin data for trading platforms ensuring data accuracy and integrity.  
- Designed and implemented automated trading scripts, achieving an average daily trading profit of **$2,000**.  
- Contributed to the development of a custom Python-based trading system for efficient trade execution and real-time market adaptation.  
- Delivered actionable insights using Bollinger Band algorithms and rule-based systems.
    """
)

expander_experience(
    "Oct 2018 – Jun 2019: Process Associate @ Genpact",
    """
**Automation-focused Professional** who streamlined data cleaning processes using Python.  
- Reduced manual processing time by **30%** while enhancing data accuracy.  
- Designed tracking systems to improve operational efficiency and enable real-time decision-making.  
- Regularly communicated insights and updates to stakeholders, driving continuous improvement in data management and operational workflows.
    """
)

expander_experience(
    "Mar 2018 – Jul 2018: Junior Technical Officer at Zoom Air, India",
    """
**Proactive Technical Officer** who optimized flight routes and collaborated with cross-functional teams.  
- Achieved significant operational cost savings by optimizing flight routes.  
- Monitored aircraft maintenance schedules meticulously to minimize downtime and enhance fleet reliability.  
- Reviewed and audited maintenance records to ensure regulatory compliance.  
- Analyzed operational needs for leasing new aircraft, contributing to improved efficiency and safety.
    """
)

# --- SKILLS ---
st.write("\n")
st.markdown(
    """
    <style>
    .skill-bar {
        position: relative;
        display: block;
        width: 100%;
        background: #e0e0e0;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .skill-bar-inner {
        height: 20px;
        border-radius: 5px;
        background: #4A90E2;
        width: 0%;
        transition: width 1s ease-in-out;
    }
    </style>
    <script>
    // Simple script to animate the skill bars after page load.
    window.onload = function() {
        const bars = document.querySelectorAll('.skill-bar-inner');
        bars.forEach(bar => {
            bar.style.width = bar.getAttribute('data-percent');
        });
    }
    </script>
    """,
    unsafe_allow_html=True,
)
# --- SKILLS ---
st.write("\n")
st.subheader("Hard Skills", anchor=False)
st.write(
    """
    - Python, SQL, PyTorch, Pandas, Numpy  
    - TensorFlow, Hugging Face, NLTK, Tableau  
    - Mlflow, Git, OpenAI, LLaMa, Prompt Engineering  
    - Google Cloud, Azure, AWS
    """
)



st.markdown(
    """
    <style>
    .navbar {
        position: sticky;
        top: 0;
        background: #ffffff;
        padding: 0.5rem 1rem;
        border-bottom: 1px solid #eaeaea;
        z-index: 100;
    }
    .navbar a {
        margin: 0 1rem;
        text-decoration: none;
        color: #4A90E2;
        font-weight: 600;
    }
    .footer {
        text-align: center;
        padding: 1rem;
        margin-top: 2rem;
        border-top: 1px solid #eaeaea;
        color: #777;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Later at the bottom of your page:
st.markdown(
    """
    <div class="footer">
        © 2025 Rajesh Goldy. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True,
)
