from fastapi import FastAPI
from server.api_routes import router
import uvicorn
from fastapi.staticfiles import StaticFiles
import tempfile
import os
# os.chdir("../")

app = FastAPI()
app.include_router(router)

temp_dir = tempfile.gettempdir()  # system temporary directory
app.mount("/static", StaticFiles(directory=temp_dir), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8501, reload=True)
