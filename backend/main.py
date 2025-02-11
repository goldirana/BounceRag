from fastapi import FastAPI
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

model  = ChatOpenAI(temperature=0.5,model="gpt-4o")
app = FastAPI()

class QueryRequest(BaseModel):
    question: str


@app.post("/query")
def query_llm(request: str):
    response = "hello world"
    return {"response": response}


@app.post("/hello")
def hello_world(request: QueryRequest):
    response = model.invoke(request.question)
    content = response.content
    return {"response": content} # return json response
