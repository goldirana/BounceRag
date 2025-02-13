import streamlit as st

# page setup
about_page = st.Page(
    page="pages/about_me.py",
    title = "👩‍💻 About Me",
    default=True,
)

query_page = st.Page(
    page="pages/query.py",
    title = "💬 Chat"
   
)

# -- Navigation --

pg = st.navigation(
    {"Info": [about_page],
     "Project": [query_page]}
)

st.logo("/Users/goldyrana/mess/deep_learning/projects/rag/frontend/assests/bounce_insight_logo.png")

pg.run()