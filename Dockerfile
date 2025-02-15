# Use an official Python runtime as a parent image
FROM python:3.9.19

# Set the working directory in the container
WORKDIR /app

# Copy the local directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable for OpenAI API key
ENV OPENAI_API_KEY= "your open ai key"


# Run both FastAPI and Streamlit using a process manager like gunicorn for FastAPI
# and streamlit's own server for Streamlit. Using a script to start both.
CMD ["/app/run_services.sh"]