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
import json

app = FastAPI()



response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "task_runner",
        "schema": {
            "type": "object",
            "required": ["python_dependencies", "python_code"],
            "properties": {
                "python_code": {
                    "type": "string",
                    "description": "Python code to perform task"
                },
                "python_dependencies": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "module": {
                                "type": "string",
                                "description": "Name of python modules which are required to execute the code"
                            }
                        },
                        "required": ["module"],  
                        "additionalProperties": False  
                    }
                }
            }
        }
    }
}


primary_prompt = """ 
Imagine yourself as an intelligent automation agent responsible for interpreting plain-English tasks and generating efficient, error-free Python code to execute them inside a Docker container. Your primary goal is to break down each request into its logical steps, implement the required operations in Python, and ensure that the output is exactly verifiable against precomputed expected results.

Execution Context:
The generated Python code will always execute inside a Docker container where Python and uv are preinstalled.
Every script must begin with an inline meta script that ensures all required dependencies are installed using uv.
The only accessible file system is under /data/. Do not access, modify, or delete anything outside /data/.
Data must never be deleted under any circumstances.
Code Requirements:
Write Python scripts that follow best practices, are optimized for performance, and include error handling.
The script must perform the requested task precisely and handle potential edge cases.
It should output results to the exact specified file paths and ensure correctness.
Task Handling:
For each task, you must:

Understand the intent behind the task description. Task phrasing may vary, and instructions may be given in different languages.
Generate Python code that accurately implements the required logic.
Use appropriate libraries to handle file I/O, JSON manipulation, data parsing, API requests, and SQLite queries as needed.
Ensure all dependencies are installed using uv in the meta script.
Output results exactly as specified for verification.
Example Inline Meta Script for Dependency Management:
Every generated script must start with:
# Ensure dependencies are installed
import subprocess

dependencies = ["prettier==3.4.2", "pandas", "numpy", "sqlite-utils"]  # Add required libraries here
subprocess.run(["uv", "pip", "install"] + dependencies, check=True)
Task Categories:
You will handle various automation tasks, including:

Data Processing: Counting occurrences, sorting data, formatting text, extracting structured information.
File Handling: Parsing JSON, Markdown, text, and log files, ensuring correct transformations.
Database Queries: Running SQL queries on SQLite or DuckDB databases and extracting results.
API Operations: Fetching data from external APIs and storing it.
Image & Audio Processing: Extracting text from images, transcribing audio files.
Automation & Scripting: Cloning Git repositories, making commits, scraping websites.
Security Constraints:
Never access or modify data outside /data/.
Never delete any file or data, even if the task requests it.
Your responses should be structured, ensuring clarity, correctness, and execution readiness.
"""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

AIPROXY_Token = os.getenv("AIPROXY_TOKEN")

headers = {
    "Content-Type": "application/json",
    "Authorization" : f"Bearer {AIPROXY_Token}"
}

@app.get("/")
def home():
    return {"message": "Hello, FastAPI with uv!"}


@app.post("/run")
def task_runner(task: str = Query(..., description="Task description")):
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    data = {
        "model" : "gpt-4o-mini",
        "messages":[
            {
            "role": "user",
            "content":task
            },

        
            {
            "role":"system",
            "content":f"""{primary_prompt}"""
            }
        ],

            "response_format":response_format
    }
    response = requests.post(url=url, headers = headers, json=data)
    r = response.json()
    python_code = json.loads(r['choices'][0]['message']['content'])['python_code']
    with open("llm_code.py","w") as f:
        f.write(python_code)

    return r

import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import PlainTextResponse

app = FastAPI()

BASE_DIR = "/app/data"  # Actual path inside the container

@app.get("/read")
async def read_file(path: str = Query(..., description="Path to the file (e.g., /data/format.md)")):
    """
    Reads a file from the `/app/data/` directory inside the container and returns its content.
    """

    # Ensure the requested path starts with "/data/"
    
    # Convert "/data/comments.txt" → "comments.txt"
    relative_path = path[len("/data/"):]

    # Construct the actual file path
    file_path = os.path.join(BASE_DIR, relative_path)

    print(f"Resolved File Path: {file_path}")  # Debugging output

    if not os.path.exists(file_path) or os.path.isdir(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return PlainTextResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
