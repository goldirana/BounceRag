#!/bin/bash
# Start FastAPI in the background
uvicorn server.main:app --host 0.0.0.0 --port 8501 &

# Start Streamlit in the foreground
streamlit run frontend/main.py --server.port=8502