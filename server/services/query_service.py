from backend.src.storage.chroma_storage import VectorDatabase
from backend.src.queries.handler import QueryHandler
from langchain.schema.document import Document
from typing import *
from langchain.schema.messages import HumanMessage
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.schema.output_parser import StrOutputParser
from backend.src.llm_models import get_openai_embeddings, get_openai_model

embeddings = get_openai_embeddings()
# vb = VectorDatabase()
# vectorstore = vb.init_chromadb(embeddings)
# retriever = vb.get_retriever(vectorstore, id_key="doc_id")
# query_handler = QueryHandler(retriever)

    

class QueryService:
    def __init__(self, embeddings, vb: VectorDatabase):
        
        self.vb = vb
        self.embeddings = embeddings
        self.chroma = self.vb.init_chromadb(self.embeddings)
        self.multi_vector_retriever = self.vb.get_multivector_retriever(self.chroma, id_key="doc_id")
        self.query_handler = QueryHandler(self.multi_vector_retriever)
        self.vectorstore_as_retriever = self.query_handler.get_vectorstore_as_retreiever()
        
    def search_similar_documents(self, query: str, top_k: int = 5) -> List[Document]:
        """Performs similarity search on vectorstore docs."""
        results = self.query_handler.similarity_search(query, top_k)
        return results

    def rag_pipeline(self: object, prompt_func, model):
        chain = (
            {"context": self.vectorstore_as_retriever | RunnableLambda(QueryHandler.split_image_text_types), "question": RunnablePassthrough()}
            | RunnableLambda(prompt_func)
            | model
            | StrOutputParser()
        )
        return chain
        
    def get_stored_docs(self, retrieved_docs: List[Document])-> dict:
        """Main function to process query using RAG"""
        data = self.query_handler.split_image_text_types(retrieved_docs)
        return data