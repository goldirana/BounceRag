from fastapi import APIRouter, Depends
from server.dependencies import (get_vector_db, get_text_summarizer, 
                                 get_image_summarizer, 
                                 get_rag_service, get_query_service,
                                 get_llm_model)
from pydantic import BaseModel


router = APIRouter()

rag_service = get_rag_service()
query_service = get_query_service()
model = get_llm_model()


class QueryRequest(BaseModel):
    question: str


@router.post("/query")
async def search_vb(request: QueryRequest):
    query = request.question
    chain = rag_service.get_chain(query, query_service, model)
    response = await chain.ainvoke(query)
    return {"response": response}