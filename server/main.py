from fastapi import FastAPI
from server.api_routes import router
import uvicorn


app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081, reload=True)