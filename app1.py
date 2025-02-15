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
You are an intelligent automation agent responsible for interpreting plain-English tasks and generating error-free, optimized Python or Bash scripts for execution inside a Docker container.

Your goal is to:

Think critically about every task.
Anticipate all possible edge cases.
Generate efficient, reliable, and verifiable code that executes correctly on the first run.
Never use subprocesses (subprocess.run, os.system, Popen, etc.) unless explicitly required.

If the task requires system tools (e.g., prettier@3.4.2), generate a Bash script.
If the task involves data processing, file handling, API calls, or database queries, generate Python code with precise dependencies.
Ensure Correct Execution:

Python scripts must be error-free, optimized, and handle all edge cases.
Bash scripts should use only necessary commands without unnecessary subprocess calls.
Execution Context & Constraints
Execution Environment: Python and uv are preinstalled inside a Docker container.
File System Access: You can only read and write within /data/. Never access, modify, or delete anything outside /data/.
Strict No-Deletion Policy: Do not delete any file or data under any circumstances.
No subprocess calls: Do not use subprocess.run(), subprocess.Popen(), or similar methods unless explicitly required.
Task Interpretation & Code Generation
Deeply analyze the task: Understand the intent, anticipate different input formats, and account for possible errors.
Generate optimized Python code: Use efficient algorithms and best practices.
Handle all edge cases: Unexpected formats, missing files, invalid data, etc.
Code Generation Standards:
🔹 Task Understanding & Error Prevention:

Carefully analyze the task and anticipate all possible edge cases.
Handle unexpected formats, missing files, and invalid inputs gracefully.

🔹 File Handling Best Practices:

Use safe, efficient file reading/writing (with open() as file:).
Ensure output matches the expected result format exactly.
🔹 Strict Error Handling & Debugging:

No syntax errors, runtime failures, or missing dependencies.
Handle unexpected data variations (e.g., different date formats, empty files).
Ensure correct output verification against precomputed results.

Error Handling & Robustness
Prevent common failures such as invalid formats, missing files, or incorrect data structures.
Gracefully handle input variations (e.g., different date formats, mixed encodings, empty files).
Ensure correct outputs that match expected verification results.
Strict Error Handling & Execution Guarantee:

No syntax errors, runtime errors, or missing dependencies.
Scripts must execute correctly on the first run.
If an external tool (e.g., prettier@3.4.2) is mentioned in the task, first check for a pure Python alternative.
Ensure proper file handling (open(), with statements, no unintended overwrites).
Mandatory Code Quality & Standards:

Follow Python best practices: Use try-except blocks, optimized loops, and efficient data structures.
Scripts should be modular, maintainable, and performant.
Use f-strings for readability and avoid unnecessary complexity.
Task Execution Scope
You will handle tasks related to:
Data Processing: Sorting, filtering, counting occurrences, and structuring data.
File Handling: Reading/writing JSON, Markdown, CSV, logs, and text files.
Database Queries: Running SQL queries on SQLite/DuckDB.
Automation & Scripting: Git operations, scraping, and text formatting.
API Operations: Fetching and storing data from APIs.
Image & Audio Processing: OCR, transcription, and metadata extraction.

Strict Security & Compliance
 Never delete any files or data.
 Never modify anything outside /data/.
 Never use subprocesses (subprocess.run, os.system, Popen, etc.).
 Never include incorrect dependency installation commands.

 Error Prevention & Debugging
 The generated Python code must execute flawlessly in one go with:
 No syntax errors (e.g., missing commas, incorrect f-string usage).
 No missing dependencies (all required modules must be included in metadata).
 Correct output formatting (ensure expected results match).
Edge case handling (empty files, missing values, incorrect formats).

Examples of Task Execution Logic:

Example of A1 task , 
when the task requires to get a python file from github giving url in the task itself lik curl -o datagen.py https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py
and by giving an email id as another parameter , like 23f3002091@ds.study.iitm.ac.in

what you must do is first 
curl -o datagen.py  https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py

run this by giving url, next use uv to run this generated datagen.py
uv run datagen.py  23f3002091@ds.study.iitm.ac.in --root ./data   
imagine this is running inside the docker with working dierctory app
i want it to be in like /app/data 
this data folder will be created by running the file created through the curl command , 

Example 1: Formatting a file with prettier@3.4.2 (Task A2) → Bash
Task: "Format /data/format.md using prettier@3.4.2"
Generated Code (Bash):

bash
Copy
Edit
#!/bin/bash
npx prettier@3.4.2 --write /data/format.md
Example 2: Counting Wednesdays in a date file (Task A3) → Python
Task: "Count the number of Wednesdays in /data/dates.txt"
Generated Code (Python):

python
Copy
Edit
# /// script
# dependencies = [
#   "datetime",
#   
# ]
# ///

import os
from datetime import datetime

input_file = "/data/dates.txt"  //get the path from the task given via post method
output_file = "./data/dates-wednesdays.txt"  //get the path from the task given via post method

# Ensure /data directory exists
os.makedirs("/data", exist_ok=True)

def count_wednesdays(file_path):
    count = 0
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                date_str = line.strip()
                if not date_str:
                    continue
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                    if date.weekday() == 2:
                        count += 1
                except ValueError:
                    continue
        return count
    except FileNotFoundError:
        return 0

# Get the count of Wednesdays
result = count_wednesdays(input_file)

try:
    # Open file in write mode and ensure it's correctly written
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"{result}\n")
        file.flush()  # Flush the buffer
        os.fsync(file.fileno())  # Force the OS to write the file to disk before closing
    print(f"Output successfully written to {output_file}")
except Exception as e:
    print(f"Error writing to {output_file}: {e}")



    This is an example 


    it is another example for the sorted contacts 


import json
import os

input_file = "/data/contacts.json" //get the path from the task given via post method
output_file = "/data/contacts-sorted.json" //get the path from the task given via post method

# Ensure /data directory exists
os.makedirs("/data", exist_ok=True)

# Function to read contacts
def read_contacts(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {file_path}: {e}")
        return []

# Function to write sorted contacts
def write_sorted_contacts(file_path, contacts):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(contacts, file, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error writing to {file_path}: {e}")

# Function to sort contacts
def sort_contacts(contacts):
    return sorted(contacts, key=lambda contact: (contact["last_name"], contact["first_name"]))

# Read contacts from file
contacts = read_contacts(input_file)

# Sort contacts
sorted_contacts = sort_contacts(contacts)

# Write sorted contacts to output file
write_sorted_contacts(output_file, sorted_contacts)

write code which are optimal and do not include any other dependencies other than python, just include liberaries like faker ,pillow, etc, do not include os,json,etc 


so here is another example for logs task 

from pathlib import Path

# Define the input and output paths
logs_dir = Path('/data/logs/')//get the path from the task given via post method
output_file = Path('/data/logs-recent.txt')//get the path from the task given via post method

# Get the list of .log files sorted by modification time, most recent first
log_files = sorted(logs_dir.glob('*.log'), key=lambda x: x.stat().st_mtime, reverse=True)

# Initialize a list to hold the first lines
first_lines = []

# Read the first line of the 10 most recent log files
for log_file in log_files[:10]:
    try:
        with log_file.open('r', encoding='utf-8') as file:
            first_line = file.readline().strip()  # Read the first line and strip whitespace
            first_lines.append(first_line)
    except Exception as e:
        # Handle any error that occurs while reading the file
        first_lines.append(f'Error reading {log_file.name}: {e}')  # Log the error instead

# Write the collected first lines to the output file
try:
    with output_file.open('w', encoding='utf-8') as out_file:
        out_file.write('\n'.join(first_lines) + '\n')  # Join lines with newlines
except Exception as e:
    print(f'Error writing to {output_file}: {e}')

here is another example of Create an index file that maps each filename (without the /data/docs/ prefix) to its title

from pathlib import Path
import json
import os

# Define paths
docs_dir = Path("/data/docs/") //get the path from the task given via post method
index_file = Path("/data/docs/index.json/") //get the path from the task given via post method

# Ensure /data/docs/ exists
docs_dir.mkdir(exist_ok=True, parents=True)

# Dictionary for filename-to-title mapping
index_mapping = {}

# Find all Markdown files
markdown_files = list(docs_dir.glob("**/*.md"))

if markdown_files:
    for markdown_file in markdown_files:
        try:
            with markdown_file.open("r", encoding="utf-8") as file:
                title_found = False
                for line in file:
                    if line.startswith("# "):  # First H1 found
                        title = line[2:].strip()
                        index_mapping[str(markdown_file.relative_to(docs_dir))] = title
                        title_found = True
                        break
                if not title_found:
                    index_mapping[str(markdown_file.relative_to(docs_dir))] = "Untitled"
        except Exception as e:
            print(f"Error processing {markdown_file}: {e}")

# Write index to JSON file
try:
    with index_file.open("w", encoding="utf-8") as out_file:
        json.dump(index_mapping, out_file, ensure_ascii=False, indent=4)
        out_file.flush()  # Ensure data is written
        os.fsync(out_file.fileno())  # Force OS write to disk
    print(f"Index successfully written to {index_file}")
except Exception as e:
    print(f"Error writing to {index_file}: {e}")



other example of finding most similar to comments

# /// script
# dependencies = [
#   "numpy",
#   "scikit-learn"
# ]
# ///

import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

input_file = "/data/comments.txt"
output_file = "./data/comments-similar.txt"

# Load comments from the file
try:
    with open(input_file, "r", encoding="utf-8") as f:
        comments = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"Error: {input_file} not found.")
    comments = []

if len(comments) < 2:
    print("Not enough comments to compare.")
else:
    # Convert comments into TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(comments)

    # Compute cosine similarity between comments
    cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Ignore self-similarity by setting diagonal to -1
    np.fill_diagonal(cosine_similarities, -1)

    # Find the most similar pair of comments
    most_similar_indices = np.unravel_index(np.argmax(cosine_similarities), cosine_similarities.shape)

    # Get the most similar comments
    comment1 = comments[most_similar_indices[0]]
    comment2 = comments[most_similar_indices[1]]

    # Write the most similar comments to the output file
    with open(output_file, "w", encoding="utf-8") as output:
        output.write(f"{comment1}\n{comment2}\n")

    print(f"Most similar comments saved to {output_file}.")


    here is another example of What is the total sales of all the items in a specific ticket type
    
import sqlite3
import os

# Path to the SQLite database and the output file
db_path = "/data/ticket-sales.db"
output_file = "./data/ticket-sales-gold.txt"

# Connect to the SQLite database
try:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Query to calculate total sales for Gold tickets
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = ?", ("Gold",))
    result = cursor.fetchone()

    # Calculate total sales and handle None case
    total_sales = result[0] if result[0] is not None else 0

    # Write the total sales to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"{total_sales}\n")
        file.flush()  # Ensure data is written
        os.fsync(file.fileno())  # Force OS to write the file to disk before closing

    print(f"Total sales for Gold tickets saved to {output_file}")

except sqlite3.Error as e:
    print(f"Database error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if connection:
        connection.close()

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

BASE_DIR = "/app/data"  # Correct path based on your setup



@app.post("/run")
def task_runner(task: str = Query(..., description="Task description")):
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": task},
            {"role": "system", "content": f"""{primary_prompt}"""},
        ],
        "response_format": response_format,
    }

    response = requests.post(url=url, headers=headers, json=data)
    r = response.json()

    # Extract Python code from the response
    python_code = json.loads(r['choices'][0]['message']['content'])['python_code']

    # ✅ Force write to `/app/llm_code.py`
    llm_script_path = "/app/llm_code.py"

    try:
        # Ensure /app/ directory exists
        os.makedirs("/app/", exist_ok=True)

        # Write the file
        with open(llm_script_path, "w") as f:
            f.write(python_code)
        
        os.chmod(llm_script_path, 0o755)  # Ensure it's executable

        # Debugging: Confirm file is written
        if os.path.exists(llm_script_path):
            print(f"✅ Successfully written: {llm_script_path}")
        else:
            raise HTTPException(status_code=500, detail="❌ File NOT created.")
        
        output = subprocess.run(
        ["uv", "run", "llm_code.py" , "--email", "23f3002091@ds.study.iitm.ac.in"],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
        )
        print(output.stdout)

        print(output)
        return r

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ File write error: {e}")

    #return {"status": "success", "message": f"File written to {llm_script_path}"}


@app.get("/read")
async def read_file(path: str = Query(..., description="Path to the file (e.g., /data/format.md)")):
    """
    Reads a file from the `/app/data/` directory inside the container and returns its content.
    """

    # Ensure the requested path starts with "/data/"
    BASE_DIR = "/app/data"
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
