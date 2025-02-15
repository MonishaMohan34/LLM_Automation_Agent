# /// script
# dependencies = [
#   "fastapi",
#   "uvicorn",
#   "requests",
#   "pillow",
#   "faker",
# 
# ]
# ///

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import os
import subprocess
import requests
import re

app = FastAPI()
BASE_DIR = "/app"  # Base directory inside the container

AIPROXY_Token = os.getenv("AIPROXY_TOKEN")
if not AIPROXY_Token:
    raise RuntimeError("AIPROXY_TOKEN environment variable is not set. Please set it before running the script.")

AI_PROXY_BASE_URL = "https://aiproxy.sanand.workers.dev/openai/v1"

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/")
def home():
    return {"message": "Hello, FastAPI with uv!"}

@app.get("/read")
async def read_file(path: str = Query(..., description="File name to read")):
    """
    Reads a file from the container's `/app` directory and returns its content.
    """
    file_path = os.path.join(BASE_DIR, path)

    if not os.path.exists(file_path) or os.path.isdir(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(file_path, "r") as file:
            content = file.read()
        return PlainTextResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

@app.post("/run")
def run(task: str = Query(..., description="Task to execute")):
    try:
        # Extract script URL & email dynamically
        script_url_match = re.search(r"https?://[^\s]+", task)
        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", task)

        if not script_url_match:
            raise HTTPException(status_code=400, detail="Script URL not found in task.")
        if not email_match:
            raise HTTPException(status_code=400, detail="User email not found in task.")

        script_url = script_url_match.group(0)
        user_email = email_match.group(0)

        # Ensure /app/data exists
        data_dir = "/app/data"
        os.makedirs(data_dir, exist_ok=True)

        # Download script
        script_path = "/app/datagen.py"

        
        response = requests.get(script_url)
        if response.status_code == 200:
            with open(script_path, "wb") as f:
                f.write(response.content)
        else:
            raise HTTPException(status_code=500, detail="Failed to download datagen.py")

        # Execute script explicitly in /app
        result = subprocess.run(
            ["uv", "run", "python", script_path, user_email],
            check=True,
            cwd="/app",
            capture_output=True,
            text=True,
            env={"DATA_DIR": "/app/data", **os.environ}
        )

        


        return {"status": "success", "message": "Data generation complete.", "output": result.stdout}

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error executing script: {e.stderr}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Ensures the app runs inside the container
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
