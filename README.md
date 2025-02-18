# RAG Project
webpage to access rag system: https://frontend-9zk7.onrender.com/ 
If you encouter 505 error, please contact at goldirana3210@gmail.com to start server again

## Project Overview
This project implements a Retrieval-Augmented Generation (RAG) system using FastAPI for the backend and Streamlit for the frontend. It provides an interface for querying and generating responses based on document content.

## Installation

### Prerequisites
- Python 3.9
- Docker (optional)

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/goldirana/BounceRag.git
   cd rag-project
   ```

2. Create and activate a virtual environment:
   ```bash
   conda create -n rag python=3.9 -y
   conda activate rag
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. Set up environment variables:
   ```bash
   export OPENAI_API_KEY="your-api-key"
   export PYTHONPATH="path_to_your_directory/rag:$PYTHONPATH"
   ```

## Running Locally

### Using Docker
1. Build the Docker image:
   ```bash
   docker build -t rag-app .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 rag-app
   ```

### Without Docker
1. Start the FastAPI backend:
   ```bash
   uvicorn server.main:app --host 0.0.0.0 --port 8000
   ```

2. Start the Streamlit frontend:
    open frontend/query.py and set the host and port as per fast api
   ```bash
   streamlit run frontend/main.py
   ```

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure settings:
   - Name: Your service name
   - Region: Select preferred region
   - Branch: main
   - Build Command: `pip install -r server/requirements.txt`
   - Start Command: `uvicorn server.main:app --host 0.0.0.0 --port $PORT`
4. Set environment variables:
   - OPENAI_API_KEY: Your OpenAI API key
5. Deploy the service

### Similarly create render for streamlit
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure settings:
   - Name: Your service name
   - Region: Select preferred region
   - Branch: main
   - Build Command: `pip install -r frontend/requirements.txt`
   - Start Command: `streamlit run frontend/main.py`
4. Set environment variables:
   - OPENAI_API_KEY: Your OpenAI API key
5. Deploy the service

## Environment Variables
| Variable         | Description                          |
|------------------|--------------------------------------|
| OPENAI_API_KEY   | API key for OpenAI services          |
| PYTHONPATH       | Python path for project modules      |

## Contributing
1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License
This project is licensed under the MIT License - see the LICENSE file for details.



## How to improve further
1. Hypothetical Questions for Better Document Filtering
   - How to:
      * 1.1 Use a question-generation model (e.g., T5 or GPT-based) to automatically generate hypothetical questions from the summaries.
      * 1.2 Store these questions alongside the embeddings in your vector database.
      * 1.3 During retrieval, match user queries not just with document embeddings but also with these hypothetical questions for better relevance.
2. Conditional Prompting Chains
   - How to:
     * 2.1 Define context-specific prompts for different tasks (e.g., comparison, summarization, extraction).
     * 2.2 Use a router chain to dynamically select the appropriate prompt based on the user's query.
     * 2.3 For tabular data, integrate libraries like pandas or tabulate to format outputs.
3. User Management with Google Authentication
   - How to:
      * 3.1 Use Firebase Authentication for Google sign-in.
      * 3.2 Store user-specific data in Firestore under unique user IDs.
      * 3.3 Implement role-based access control (e.g., admin, user) if needed.
4. Experiment with Prompt Design
   - How to:
      * 4.1 Currently system Use few-shot prompting to guide the model with examples in some scenario but can be extended
      * 4.2 Test chain-of-thought (CoT) prompting for complex reasoning tasks.
      * 4.3 Explore instruction tuning to make the model follow specific instructions better.
      * 4.4 Currently system uses RoR (Rephrase and Respond) to redefine the user query, however this can be tested with different prompts
5. Hybrid Search
   - How to:
      * 5.1 Combine vector search (semantic similarity) with keyword-based search (BM25) for better retrieval accuracy.
      * 5.2 Libraries like Weaviate or Pinecone support hybrid search out of the box. (Currently system uses chromadb because of free version but pinecone can be used to improve memory because of cloud storage of pinecone)
6. Caching for Frequent Queries
   - How to:
      * 6.1 Cache frequently asked queries and their responses to reduce latency and API costs.
      * 6.2 Use tools like Redis or Memcached for efficient caching.
      * 6.3 Store these questions alongside the embeddings in your vect

