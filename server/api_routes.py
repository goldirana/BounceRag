from fastapi import APIRouter, Depends
from server.dependencies import get_vector_db, get_text_summarizer, get_image_summarizer
from server.services.rag_service import RAGService
from server.services.query_service import QueryService
from pydantic import BaseModel


router = APIRouter()
query_service = QueryService()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
def search_vb(request: QueryRequest):
    retrieved_docs = query_service.search_similar_documents(request.question, top_k=5)
    raw_docs, metadata = query_service.query_handler.map_raw_docs(retrieved_docs)
    return {"response": response}