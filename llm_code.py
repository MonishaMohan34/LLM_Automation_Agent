# Ensure dependencies are installed
import subprocess

dependencies = ["prettier==3.4.2"]  # Add required libraries here
subprocess.run(["uv", "pip", "install"] + dependencies, check=True)

import os

# Define the file path
file_path = '/data/format.md'

# Check if the file exists in the specified path
if not os.path.isfile(file_path):
    raise FileNotFoundError(f'The file {file_path} does not exist.')

# Read the contents of the file
with open(file_path, 'r') as file:
    contents = file.read()

# Format the contents using Prettier in a subprocess
result = subprocess.run(["uv", "prettier", "--write", file_path], 
                        input=contents, text=True, capture_output=True)

# Check if the formatting was successful
if result.returncode != 0:
    raise RuntimeError(f'Prettier formatting failed: {result.stderr}')