import requests

FASTAPI_URL = "http://127.0.0.1:8085"

def hello(query: str):
    print("i am fron api.py")
    response = requests.post(f"{FASTAPI_URL}/query", json={"question": query})
    return response.json()["response"]

def hello_world(query: str):
    response = requests.post(f"{FASTAPI_URL}/hello", json={"question": query})
    try:
        return response.json().get("response", "Error: No response received from FastAPI")
    except Exception as e:
        return {"error": f"Failed to parse FastAPI response: {str(e)}"}
    
    