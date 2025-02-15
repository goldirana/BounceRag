# # Use official Python image
# FROM python:3.9.19

# # Set working directory
# WORKDIR /app


# # Copy the entire project
# COPY . /app

# # # Copy requirements file
# # COPY requirements.txt .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Install supervisord for process management
# RUN apt-get update && apt-get install -y supervisor
# COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# # Expose port
# EXPOSE 8502

# # Start services
# CMD ["supervisord", "-n"]

# Use an official Python runtime as a parent image
FROM python:3.9.19

# Set the working directory in the container
WORKDIR /app

# Copy the local directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt
# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable for OpenAI API key
ENV OPENAI_API_KEY="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" 


# Run both FastAPI and Streamlit using a process manager like gunicorn for FastAPI
# and streamlit's own server for Streamlit. Using a script to start both.
CMD ["/app/run_services.sh"]