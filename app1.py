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
 Task Understanding & Error Prevention:

Carefully analyze the task and anticipate all possible edge cases.
Handle unexpected formats, missing files, and invalid inputs gracefully.

 File Handling Best Practices:

Use safe, efficient file reading/writing (with open() as file:).
Ensure output matches the expected result format exactly.
 Strict Error Handling & Debugging:

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


here is example python code 
import os
import urllib.request

# Define the URL and output file
url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
output_file = "./data/datagen.py"

# Ensure /data directory exists
os.makedirs("./data", exist_ok=True)

# Download the Python script
try:
    urllib.request.urlretrieve(url, output_file)
    print(f"Downloaded script to {output_file}")
except Exception as e:
    print(f"Error downloading the script: {e}")

# Run the downloaded Python script with uv
email_argument = "23f3002091@ds.study.iitm.ac.in"
try:
    os.system(f"uv run {output_file} {email_argument} --root ./data")
except Exception as e:
    print(f"Error running the script: {e}")


Example for task A2:
Formatting a file with prettier@3.4.2 (Task A2) → Bash
Task: "Format /data/format.md using prettier@3.4.2"

Copy
Edit
run this bash command 
//get file name from the user 
npx prettier@3.4.2 --write /data/format.md


Example for task A3 ,this is an example code , just understand the task and create such that the given task is completed correctly

from datetime import datetime
from dateutil.parser import parse

input_file = "./data/dates.txt"
output_file = "./data/dates-wednesdays.txt"

# List of date formats to check explicitly
date_formats = [
    "%Y-%m-%d",
    "%d-%b-%Y",
    "%m/%d/%Y",
    "%d/%m/%Y",
    "%B %d, %Y",
    "%Y/%m/%d %H:%M:%S",
    "%Y-%m-%d %H:%M:%S",
    "%d-%b-%Y %H:%M:%S",
    "%b %d, %Y"
]

# Function to parse a date string
def parse_date(date_str):
    date_str = date_str.strip()
    if not date_str:
        return None
    # Try all known formats first
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    # If no format matched, try the generic parser
    try:
        return parse(date_str, fuzzy=True)
    except ValueError:
        return None

# Function to count Wednesdays in the provided date file
def count_wednesdays(file_path):
    count = 0
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                date = parse_date(line)
                if date and date.weekday() == 2:  # 2 = Wednesday
                    count += 1
        return count
    except FileNotFoundError:
        return 0

# Get the count of Wednesdays
result = count_wednesdays(input_file)

# Write the result to the output file
try:
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"{result}\n")
except Exception as e:
    print(f"Error writing to {output_file}: {e}")


This is an example 


it is another example for the sorted contacts 


import json
import os

input_file = "./data/contacts.json" //get the path from the task given via post method
output_file = "./data/contacts-sorted.json" //get the path from the task given via post method

# Ensure /data directory exists
os.makedirs("./data", exist_ok=True)

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
logs_dir = Path('./data/logs/')//get the path from the task given via post method
output_file = Path('./data/logs-recent.txt')//get the path from the task given via post method

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
copy and edit as per the task requirment

from pathlib import Path
import json

# Define paths
docs_dir = Path("./data/docs")
index_file = Path("./data/docs/index.json")

# Ensure /data/docs/ exists
if not docs_dir.exists():
    docs_dir.mkdir(parents=True, exist_ok=True)  # Use `exist_ok=True` to avoid errors if the folder exists

# Dictionary for filename-to-title mapping
index_mapping = {}

# Find all Markdown files
markdown_files = list(docs_dir.glob('**/*.md'))

if markdown_files:
    for markdown_file in markdown_files:
        try:
            with markdown_file.open('r', encoding='utf-8') as file:
                title_found = False
                for line in file:
                    if line.startswith('# '):  # First H1 found
                        title = line[2:].strip()
                        index_mapping[markdown_file.relative_to(docs_dir).as_posix()] = title
                        title_found = True
                        break
                if not title_found:
                    index_mapping[markdown_file.relative_to(docs_dir).as_posix()] = 'Untitled'
        except Exception as e:
            index_mapping[markdown_file.relative_to(docs_dir).as_posix()] = f'Error: {e}'  # Capture any errors

# Write index to JSON file
try:
    with index_file.open('w', encoding='utf-8') as out_file:
        json.dump(index_mapping, out_file, ensure_ascii=False, indent=4)
    print(f'Index successfully written to {index_file}')
except Exception as e:
    print(f'Error writing to {index_file}: {e}')

    
here is another example of task A7: which is extracting emails of sender , receiver  and CC

according to the task requiremnets copy and edit it to return only what is asked 

import re
import os

# Define input and output file paths
input_file = "./data/email.txt"    //get from user
output_file = "./data/email-sender.txt"  //get from user

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Function to extract email addresses from different fields
def extract_emails(content, field):
    pattern = rf"^{field}:\s+(.+)$"
    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        return []
    
    # Extract email addresses from the matched line
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, match.group(1))
    return emails

# Read the email content
try:
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()
except FileNotFoundError:
    print(f"Error: {input_file} not found.")
    exit(1)

# Extract different types of email addresses
sender_email = extract_emails(content, "From")
receiver_emails = extract_emails(content, "To")
cc_emails = extract_emails(content, "Cc")

# Debugging Output
print(f"Sender Email: {sender_email}")
print(f"Receiver Emails: {receiver_emails}")
print(f"CC Emails: {cc_emails}")

# Save the extracted emails to a file
with open(output_file, "w", encoding="utf-8") as file:
    file.write(f"Sender: {', '.join(sender_email)}\n")
    file.write(f"To: {', '.join(receiver_emails)}\n")
    file.write(f"Cc: {', '.join(cc_emails)}\n")

print(f"Email details extracted and saved to {output_file}")

here is an example of the retrieving details from .png

import pytesseract
from PIL import Image
import re
input_image = "./data/credit_card.png"
output_file = "./data/credit-card.txt"

# Load the image
try:
    image = Image.open(input_image)
except FileNotFoundError:
    print(f"Error: File '{input_image}' not found.")
    exit()

# Perform OCR
extracted_text = pytesseract.image_to_string(image, config='--psm 6')

# Extract only digits (credit card number)
credit_card_number = "".join(re.findall(r'\d+', extracted_text))

# Save to output file
if credit_card_number:
    with open(output_file, "w") as f:
        f.write(credit_card_number)
    print(f"Extracted credit card number saved to {output_file}.")
else:
    print("No credit card number found.")


other example of finding most similar to comments
again this is just an eample code , copy and modify it according to the task if required 

import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

input_file = "./data/comments.txt"
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
    # Load a pre-trained sentence transformer model
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Efficient and accurate

    # Compute embeddings
    embeddings = model.encode(comments, normalize_embeddings=True)

    # Compute cosine similarity
    cosine_similarities = cosine_similarity(embeddings)

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
db_path = "./data/ticket-sales.db"
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

for task B5. Run a SQL query on a SQLite or DuckDB database

here is an example code 

def run_sql_query(
    database_file: str,
    query: str,
    output_file: Optional[str],
    database_type: str,
    output_format: str = "csv",
):

    if database_type == "sqlite":
        conn = sqlite3.connect(database_file)
    elif database_type == "duckdb":
        conn = duckdb.connect(database_file)
    else:
        raise ValueError("Unsupported database type. Use 'sqlite' or 'duckdb'.")

    try:
        result = pd.read_sql_query(query, conn)
    except Exception as e:
        conn.close()
        raise ValueError(f"Error executing query: {e}")
    finally:
        conn.close()

    # Save output if requested
    if output_file:
        if output_format == "csv":
            result.to_csv(output_file, index=False, header=True)  # CSV includes headers
        elif output_format == "txt":
            with open(output_file, "w") as file:
                for _, row in result.iterrows():
                    # Write rows without column names
                    file.write(" ".join(map(str, row.values)) + "\n")
        else:
            raise ValueError("Unsupported output format. Use 'csv' or 'txt'.")
    else:
        for _, row in result.iterrows():
            print(" ".join(map(str, row.values)))
            return {
                "output_saved_to_location": output_file,
                "response": "Task Done Successfully.",
            }

    return [{"response": result}]

for image analysis task use this code: ```

from openai import OpenAI
import base64
import os
from dotenv import load_dotenv

load_dotenv()


        # Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

        # Path to your image
image_path = "data/example.png"

        # Getting the base64 string
base64_image = encode_image(image_path)

client = OpenAI(
    api_key=os.environ.get("OPENAI_KEY"),
    base_url=os.environ.get("OPENAI_URL")
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Prompt according to task"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
    temperature=0.2,
    model="gpt-4o-mini",
)

print(chat_completion.choices[0].message.content)
        ```
        

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
    Reads a file from either `/app/data/` or `/data/` inside the container and returns its content.
    """

    BASE_DIRS = ["/app/data", "/data"]  # Prioritize /app/data, then check /data
    relative_path = path[len("/data/"):]  # Extract filename

    file_path = None

    # Check in both directories
    for base_dir in BASE_DIRS:
        potential_path = os.path.join(base_dir, relative_path)
        if os.path.exists(potential_path) and not os.path.isdir(potential_path):
            file_path = potential_path
            break  # Stop checking once we find the file

    if file_path is None:
        raise HTTPException(status_code=404, detail="File not found in both /app/data and /data")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return PlainTextResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")



# @app.get("/read")
# async def read_file(path: str = Query(..., description="Path to the file (e.g., /data/format.md)")):
#     """
#     Reads a file from the `/app/data/` directory inside the container and returns its content.
#     """

#     # Ensure the requested path starts with "/data/"
#     BASE_DIR = "/app/data"
#     # Convert "/data/comments.txt" → "comments.txt"
#     relative_path = path[len("/data/"):]

#     # Construct the actual file path
#     file_path = os.path.join(BASE_DIR, relative_path)

#     print(f"Resolved File Path: {file_path}")  # Debugging output

#     if not os.path.exists(file_path) or os.path.isdir(file_path):
#         raise HTTPException(status_code=404, detail="File not found")

#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             content = file.read()
#         return PlainTextResponse(content=content)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
