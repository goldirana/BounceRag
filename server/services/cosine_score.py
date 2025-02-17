from sklearn.metrics.pairwise import cosine_similarity
from backend.src.llm_models import (get_openai_embeddings)
import numpy as np
import torch.nn.functional as F
import torch

def get_top_matching_documents(documents, query, top_n=5):
    """
    Finds the top N documents with the highest cosine similarity to the query.

    Args:
        query (str): The query to compare against documents.
        documents (list of langchain.documents.Document): List of langchain documents.
        top_n (int): The number of top documents to return.

    Returns:
        list of langchain.documents.Document: The top N documents based on the highest similarity scores.
    """
    if not documents:
        return []  # Handle empty document list

    # Extract content from documents
    doc_texts = [doc.page_content for doc in documents]
    embedding = get_openai_embeddings()
    
    query_embedding = embedding.embed_query(query) 
    doc_embeddings = embedding.embed_documents(doc_texts)  

    similarities = cosine_similarity([query_embedding], doc_embeddings)[0]

    # Sort documents by descending similarity scores
    sorted_docs = [doc for _, doc in sorted(zip(similarities, documents), 
                                            key=lambda pair: pair[0], 
                                            reverse=True)]
    
    # Return the top N documents
    return sorted_docs[:top_n]


