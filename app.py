# /// script
# dependencies = [
#   "fastapi",
#   "uvicorn",
#   "requests",
#   "re",
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
    """
    Extracts the script URL and user email from the task description,
    downloads and executes the script inside the container.
    """
    try:
        # Extract script URL
        script_url_match = re.search(r"https?://[^\s]+", task)
        if not script_url_match:
            raise HTTPException(status_code=400, detail="Script URL not found in task.")
        script_url = script_url_match.group(0)

        # Extract email
        email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", task)
        if not email_match:
            raise HTTPException(status_code=400, detail="User email not found in task.")
        user_email = email_match.group(0)

        # Ensure uv is installed
        subprocess.run(["uv", "--version"], check=False)

        # Download script
        script_path = os.path.join(BASE_DIR, "datagen.py")
        response = requests.get(script_url)
        if response.status_code == 200:
            with open(script_path, "wb") as f:
                f.write(response.content)
        else:
            raise HTTPException(status_code=500, detail="Failed to download datagen.py")

        # Execute script
        #subprocess.run(["uv", script_path, user_email], check=True)
        os.chmod(script_path, 0o755)
        result = subprocess.run(
            ["uv", "run", "python", script_path, user_email],
            check=True,
            capture_output=True,
            text=True
        )

        return {"status": "success", "message": "Data generation complete."}

    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Error executing script: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# Ensures the app runs inside the container
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



