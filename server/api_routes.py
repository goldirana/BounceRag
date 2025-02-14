from fastapi import APIRouter, Depends
from pydantic import BaseModel
from server.dependencies import (get_vector_db, get_text_summarizer, 
                                 get_image_summarizer, 
                                 get_rag_service, get_query_service,
                                 get_llm_model, 
                                 get_firestore_chat_client)
import os
import asyncio
from fastapi.responses import StreamingResponse
from fastapi import FastAPI, Request


router = APIRouter()

firestore_chat_history = get_firestore_chat_client()
rag_service = get_rag_service()
query_service = get_query_service()
model = get_llm_model()


class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def search_vb(request: QueryRequest):

    query = request.question
    # print("DEBUG serch vb")
    # print("--"*100)
    # print(query)
    # print("--"*100)
    chain = rag_service.get_chain(query, query_service, model)
    response_data = await chain.ainvoke(query)
    
    if not isinstance(response_data, dict):  
        return {"error": "Invalid response format", "response": response_data}

    text_response = response_data.get("response", "No response generated.")
    image_urls = [f"/static/{os.path.basename(img_path)}" 
                  for img_path in response_data.get("image_paths", [])]

    firestore_chat_history.add_user_message(query)
    firestore_chat_history.add_ai_message(text_response)

    return {
        "response": text_response,
        "images": image_urls
        
    }