# from backend.src.storage.chroma_storage import VectorDatabase
from server.services.chroma_service import VectorDatabase 
from backend.src.queries.handler import QueryHandler
from langchain.schema.document import Document
from typing import *
from langchain.schema.messages import HumanMessage
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.schema.output_parser import StrOutputParser
from backend.src.llm_models import get_openai_embeddings, get_openai_model

embeddings = get_openai_embeddings()

    

class QueryService:
    """QueryService class provides methods to interact with a vector database for document retrieval and processing.
    Attributes:
        vb (VectorDatabase): An instance of the VectorDatabase class.
        embeddings: Embeddings used for initializing the vector database.
        chroma: Initialized ChromaDB instance.
        multi_vector_retriever: Multi-vector retriever instance.
        query_handler (QueryHandler): An instance of the QueryHandler class.
        vectorstore_as_retriever: Retriever for vector store.
    Methods:
        __init__(self, embeddings, vb: VectorDatabase):
            Initializes the QueryService with embeddings and a vector database.
        search_similar_documents(self, query: str, top_k: int = 5) -> List[Document]:
        # rag_pipeline(self: object, prompt_func, model):
        get_stored_docs(self, retrieved_docs: List[Document]) -> dict:
    """
    def __init__(self, embeddings, vb: VectorDatabase):
        
        self.vb = vb
        self.embeddings = embeddings
        self.chroma = self.vb.init_chromadb(self.embeddings)
        self.multi_vector_retriever = self.vb.get_multivector_retriever(self.chroma, id_key="doc_id")
        self.query_handler = QueryHandler(self.multi_vector_retriever)
        self.vectorstore_as_retriever = self.query_handler.get_vectorstore_as_retreiever()
        
    def search_similar_documents(self, query: str, top_k: int = 5) -> List[Document]:
        """
        Performs a similarity search on vectorstore documents.

        Args:
            query (str): The query string to search for similar documents.
            top_k (int, optional): The number of top similar documents to return. Defaults to 5.

        Returns:
            List[Document]: A list of documents that are most similar to the query.
        """
        results = self.query_handler.similarity_search(query, top_k)
        return results

        
    def get_stored_docs(self, retrieved_docs: List[Document])-> dict:
        """
        Retrieves and processes stored documents.
        Args:
            retrieved_docs (List[Document]): A list of Document objects to be processed.
        Returns:
            dict: A dictionary containing the processed data.
        """
        data = self.query_handler.split_image_text_types(retrieved_docs)
        return data
    
    
    # def rag_pipeline(self: object, prompt_func, model):
    #     """
    #     Constructs and returns a processing chain for the RAG (Retrieval-Augmented Generation) pipeline.
    #     Args:
    #         self (object): The instance of the class containing this method.
    #         prompt_func (callable): A function to generate prompts for the model.
    #         model (object): The model to be used in the pipeline.
    #     Returns:
    #         chain: A processing chain 
    #         that includes context retrieval, prompt generation, model inference, and output parsing.
    #     """
        
    #     chain = (
    #         {"context": self.vectorstore_as_retriever | RunnableLambda(QueryHandler.split_image_text_types), 
    #          "question": RunnablePassthrough()}
    #         | RunnableLambda(prompt_func)
    #         | model
    #         | StrOutputParser()
    #     )
    #     return chain