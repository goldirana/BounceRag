# Use an official Python runtime as a parent image
FROM python:3.9.19

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy configuration files
COPY config.yaml /app/
COPY params.yaml /app/

# Make ports 80 and 8501 available to the world outside this container
# EXPOSE 80
# EXPOSE 8501

EXPOSE $PORT
# Define environment variable
ENV NAME bounce

# Run both FastAPI and Streamlit when the container launches
# CMD ["sh", "-c", "uvicorn server.main:app --host 0.0.0.0 --port 80 & streamlit run frontend/main.py --server.port 8501"]

CMD ["sh", "-c", "uvicorn server.main:app --host 0.0.0.0 --port $PORT & streamlit run frontend/main.py --server.port $PORT"]