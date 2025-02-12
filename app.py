

# /// script
# dependencies = [
#   "fastapi",
#   "uvicorn",
#   "requests",
# ]
# ///

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException, Query
import os
from fastapi.responses import PlainTextResponse

app = FastAPI()


BASE_DIR = "/app"  # Base directory inside the container

@app.get("/read")
async def read_file(path: str = Query(..., description="File name to read")):
    file_path = os.path.join(BASE_DIR, path)

    if not os.path.exists(file_path) or os.path.isdir(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(file_path, "r") as file:
            content = file.read()
        return PlainTextResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def home():
    return {"message": "Hello, FastAPI with uv!"}
    

@app.get("/run")
def run():
    return {"message": "Hello, FastAPI with this is run!"}

# This ensures the app runs when executed with `uv run`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

