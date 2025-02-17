from sklearn.metrics.pairwise import cosine_similarity
from backend.src.llm_models import (get_openai_embeddings)
import numpy as np

def get_top_matching_documents(documents, query, top_n=2):
    """
    Finds the top N documents with the highest cosine similarity to the query.

    Args:
        model: The model to use for embeddings.
        query (str): The query to compare against documents.
        documents (list of dict): Each document should be a dict with 'content' and 'metadata'.
        top_n (int): The number of top documents to return.

    Returns:
        list of dict: The top N documents based on the highest similarity scores.
    """
    if not documents:
        return []  # Handle empty document list

    # Extract content from documents
    doc_texts = [doc.page_content for doc in documents]
    embedding = get_openai_embeddings()
    
    query_embedding = embedding.embed_query(query) 
    doc_embeddings = embedding.embed_documents(doc_texts)  

    similarities = cosine_similarity([query_embedding], doc_embeddings)[0]

    # Get indices of the top N highest similarity scores
    top_indices = np.argsort(similarities)[-top_n:][::-1]

    top_docs = [documents[i] for i in top_indices]    
    return top_docs
