from server.dependencies import *
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from backend.src.queries.handler import QueryHandler
from langchain.schema.document import Document
from typing import *
from langchain.schema.messages import HumanMessage
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.schema.output_parser import StrOutputParser


embeddings = OpenAIEmbeddings()
# vb = VectorDatabase()
# vectorstore = vb.init_chromadb(embeddings)
# retriever = vb.get_retriever(vectorstore, id_key="doc_id")
# query_handler = QueryHandler(retriever)


def prompt_func(dict):
    format_texts = "\n".join(dict["context"]["texts"])
    return [
        HumanMessage(
            content=[
                {"type": "text", "text": f"""Answer the question based only on the following context, which can include text, tables, and the below image:
                Question: {dict["question"]}

                Text and tables:
                {format_texts}
                            """},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{dict['context']['images'][0]}"}},
                    ]
                    )
            ]
    

class QueryService:
    def __init__(self):
        self.vb = get_vector_db()
        self.chroma = self.vb.init_chromadb(embeddings)
        self.multi_vector_retriever = self.vb.get_multivector_retriever(self.chroma, id_key="doc_id")
        self.query_handler = QueryHandler(self.multi_vector_retriever)
        self.vectorstore_as_retriever = self.query_handler.get_vectorstore_as_retreiever()
        
    def search_similar_documents(self, query: str, top_k: int = 5) -> List[Document]:
        """Performs similarity search on the vector database."""
        results = self.query_handler.similarity_search(query, top_k)
        return results

    # def process_query(self, retrieved_docs: List[Document]):
    #     """Main function to process query using RAG"""
    #     raw_docs, metadata = self.query_handler.map_raw_docs(retrieved_docs)
    #     images, text = self.query_handler.split_image_text_types(retrieved_docs)
    #     response = {
    #         "raw": query,
    #         "retrieved_texts": raw_text,
    #         "metadata": metadata
    #     }
    #     return response
    

    def rag_pipeline(self, retriever: object, prompt_func, model):
        chain = (
            {"context": self.vectorstore_as_retriever | RunnableLambda(QueryHandler.split_image_text_types), "question": RunnablePassthrough()}
            | RunnableLambda(prompt_func)
            | model
            | StrOutputParser()
        )
        return chain
        
    def process_query(self, retrieved_docs: List[Document]):
        """Main function to process query using RAG"""
        raw_docs, metadata = self.query_handler.map_raw_docs(retrieved_docs)
        
        
        images, images_metadata, texts, texts_metadata = self.query_handler.split_image_text_types(retrieved_docs)
        response = {
            "raw": query,
            "retrieved_texts": raw_text,
            "metadata": metadata
        }
        return response