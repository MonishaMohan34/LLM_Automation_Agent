# /// script
# dependencies = [
#   "requests",
#   "pillow",
#   "faker"
# ]
# ///

import requests

# Define the URL and parameters
url = "https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py"
email = "23f3002091@ds.study.iitm.ac.in"

# Function to download the script
def download_script(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except requests.RequestException as e:
        print(f"Error downloading script: {e}")
        return None

# Function to execute the downloaded script safely
def execute_script(script_content, email):
    global_vars = {"__name__": "__main__", "email": email}
    try:
        exec(script_content, global_vars)
    except Exception as e:
        print(f"Error executing script: {e}")

# Download the script
script_content = download_script(url)

# Execute if download was successful
if script_content:
    execute_script(script_content, email)



# import sqlite3
# import os

# # Path to the SQLite database and the output file
# db_path = "/data/ticket-sales.db"
# output_file = "./data/ticket-sales-bronze.txt"

# # Connect to the SQLite database
# try:
#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()

#     # Query to calculate total sales for Bronze tickets
#     cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = ?", ("Bronze",))
#     result = cursor.fetchone()

#     # Calculate total sales and handle None case
#     total_sales = result[0] if result[0] is not None else 0

#     # Write the total sales to the output file
#     with open(output_file, "w", encoding="utf-8") as file:
#         file.write(f"{total_sales}\n")
#         file.flush()  # Ensure data is written
#         os.fsync(file.fileno())  # Force the OS to write the file to disk before closing

#     print(f"Total sales for Bronze tickets saved to {output_file}")

# except sqlite3.Error as e:
#     print(f"Database error: {e}")
# except Exception as e:
#     print(f"Error: {e}")
# finally:
#     if 'connection' in locals():
#         connection.close()



# import sqlite3
# import os

# # Path to the SQLite database and the output file
# db_path = "/data/ticket-sales.db"
# output_file = "./data/ticket-sales-gold.txt"

# # Connect to the SQLite database
# try:
#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()

#     # Query to calculate total sales for Gold tickets
#     cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = ?", ("Gold",))
#     result = cursor.fetchone()

#     # Calculate total sales and handle None case
#     total_sales = result[0] if result[0] is not None else 0

#     # Write the total sales to the output file
#     with open(output_file, "w", encoding="utf-8") as file:
#         file.write(f"{total_sales}\n")
#         file.flush()  # Ensure data is written
#         os.fsync(file.fileno())  # Force OS to write the file to disk before closing

#     print(f"Total sales for Gold tickets saved to {output_file}")

# except sqlite3.Error as e:
#     print(f"Database error: {e}")
# except Exception as e:
#     print(f"Error: {e}")
# finally:
#     if connection:
#         connection.close()





# # /// script
# # dependencies = [
# #   "numpy",
# #   "scikit-learn"
# # ]
# # ///

# import os
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# input_file = "/data/comments.txt"
# output_file = "./data/comments-similar.txt"

# # Load comments from the file
# try:
#     with open(input_file, "r", encoding="utf-8") as f:
#         comments = [line.strip() for line in f if line.strip()]
# except FileNotFoundError:
#     print(f"Error: {input_file} not found.")
#     comments = []

# if len(comments) < 2:
#     print("Not enough comments to compare.")
# else:
#     # Convert comments into TF-IDF vectors
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(comments)

#     # Compute cosine similarity between comments
#     cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

#     # Ignore self-similarity by setting diagonal to -1
#     np.fill_diagonal(cosine_similarities, -1)

#     # Find the most similar pair of comments
#     most_similar_indices = np.unravel_index(np.argmax(cosine_similarities), cosine_similarities.shape)

#     # Get the most similar comments
#     comment1 = comments[most_similar_indices[0]]
#     comment2 = comments[most_similar_indices[1]]

#     # Write the most similar comments to the output file
#     with open(output_file, "w", encoding="utf-8") as output:
#         output.write(f"{comment1}\n{comment2}\n")

#     print(f"Most similar comments saved to {output_file}.")


# # /// script
# # dependencies = [
# #   "pytesseract",
# #   "pillow",
# #   "tesseract"
# # ]
# # ///

# import pytesseract
# from PIL import Image
# import os

# # Define input and output file paths
# input_image_path = "/data/credit_card.png"
# output_text_path = "./data/credit-card.txt"

# # Function to extract credit card number from image using OCR
# def extract_credit_card_number(image_path):
#     try:
#         # Open the image file
#         with Image.open(image_path) as img:
#             # Use pytesseract to do OCR on the image
#             text = pytesseract.image_to_string(img)
#             # Extract digits from the text
#             card_number = "".join(filter(str.isdigit, text))
#             return card_number
#     except Exception as e:
#         print(f"Error processing image {image_path}: {e}")
#         return None

# # Function to write the extracted card number to a text file
# def write_card_number_to_file(card_number, output_path):
#     try:
#         with open(output_path, "w", encoding="utf-8") as file:
#             file.write(card_number)
#     except Exception as e:
#         print(f"Error writing to file {output_path}: {e}")

# # Extract the card number
# card_number = extract_credit_card_number(input_image_path)
# if card_number:
#     # Write the card number to the output file
#     write_card_number_to_file(card_number, output_text_path)
#     print(f"Card number extracted and written to {output_text_path}")
# else:
#     print("No card number found in the image.")




# import re
# import os

# input_file = "/data/email.txt"  # File containing the email message
# output_file = "./data/email-sender.txt"  # File to write the sender's email

# # Ensure /data directory exists
# os.makedirs("/data", exist_ok=True)

# def extract_sender_email(file_path):
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             content = file.read()  # Read entire email content
#             # Use regex to find the email address
#             match = re.search(r'From: (.+?)\r?\n', content)
#             if match:
#                 return match.group(1).strip()  # Return the sender's email if found
#             else:
#                 return ""  # Return empty string if no match
#     except Exception as e:
#         print(f"Error reading {file_path}: {e}")
#         return ""  # Handle exceptions

# # Extract the sender's email address
# sender_email = extract_sender_email(input_file)

# # Write the extracted email to the output file
# try:
#     with open(output_file, "w", encoding="utf-8") as file:
#         file.write(sender_email + '\n')
#         file.flush()  # Ensure data is written
#         os.fsync(file.fileno())  # Force OS write to disk before closing
#     print(f"Sender email successfully written to {output_file}")
# except Exception as e:
#     print(f"Error writing to {output_file}: {e}")

# from pathlib import Path
# import json
# import os

# # Define paths
# docs_dir = Path("/data/docs/")
# index_file = Path("./data/docs/index.json/")

# # Ensure /data/docs/ exists
# docs_dir.mkdir(exist_ok=True, parents=True)

# # Dictionary for filename-to-title mapping
# index_mapping = {}

# # Find all Markdown files
# markdown_files = list(docs_dir.glob("**/*.md"))

# if markdown_files:
#     for markdown_file in markdown_files:
#         try:
#             with markdown_file.open("r", encoding="utf-8") as file:
#                 title_found = False
#                 for line in file:
#                     if line.startswith("# "):  # First H1 found
#                         title = line[2:].strip()
#                         index_mapping[str(markdown_file.relative_to(docs_dir))] = title
#                         title_found = True
#                         break
#                 if not title_found:
#                     index_mapping[str(markdown_file.relative_to(docs_dir))] = "Untitled"
#         except Exception as e:
#             print(f"Error processing {markdown_file}: {e}")

# # Write index to JSON file
# try:
#     with index_file.open("w", encoding="utf-8") as out_file:
#         json.dump(index_mapping, out_file, ensure_ascii=False, indent=4)
#         out_file.flush()  # Ensure data is written
#         os.fsync(out_file.fileno())  # Force OS write to disk
#     print(f"Index successfully written to {index_file}")
# except Exception as e:
#     print(f"Error writing to {index_file}: {e}")


# from pathlib import Path

# # Define the input and output paths
# logs_dir = Path('/data/logs/')
# output_file = Path('./data/logs-recent.txt')

# # Get the list of .log files sorted by modification time, most recent first
# log_files = sorted(logs_dir.glob('*.log'), key=lambda x: x.stat().st_mtime, reverse=True)

# # Initialize a list to hold the first lines
# first_lines = []

# # Read the first line of the 10 most recent log files
# for log_file in log_files[:10]:
#     try:
#         with log_file.open('r', encoding='utf-8') as file:
#             first_line = file.readline().strip()  # Read the first line and strip whitespace
#             first_lines.append(first_line)
#     except Exception as e:
#         # Handle any error that occurs while reading the file
#         first_lines.append(f'Error reading {log_file.name}: {e}')  # Log the error instead

# # Write the collected first lines to the output file
# try:
#     with output_file.open('w', encoding='utf-8') as out_file:
#         out_file.write('\n'.join(first_lines) + '\n')  # Join lines with newlines
# except Exception as e:
#     print(f'Error writing to {output_file}: {e}')




# # /// script
# # dependencies = [
# #   
# #
# # ]
# # ///

# import json
# import os

# input_file = "/data/contacts.json"
# output_file = "/data/contacts-sorted.json"

# # Ensure /data directory exists
# os.makedirs("/data", exist_ok=True)

# # Function to read contacts
# def read_contacts(file_path):
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             return json.load(file)
#     except (FileNotFoundError, json.JSONDecodeError) as e:
#         print(f"Error reading {file_path}: {e}")
#         return []

# # Function to write sorted contacts
# def write_sorted_contacts(file_path, contacts):
#     try:
#         with open(file_path, "w", encoding="utf-8") as file:
#             json.dump(contacts, file, ensure_ascii=False, indent=4)
#     except IOError as e:
#         print(f"Error writing to {file_path}: {e}")

# # Function to sort contacts
# def sort_contacts(contacts):
#     return sorted(contacts, key=lambda contact: (contact["last_name"], contact["first_name"]))

# # Read contacts from file
# contacts = read_contacts(input_file)

# # Sort contacts
# sorted_contacts = sort_contacts(contacts)

# # Write sorted contacts to output file
# write_sorted_contacts(output_file, sorted_contacts)



# # /// script
# # dependencies = [
# #   "datetime",
# #   
# # ]
# # ///

# import os
# from datetime import datetime

# input_file = "/data/dates.txt"
# output_file = "./data/dates-wednesdays.txt"

# # Ensure /data directory exists
# os.makedirs("/data", exist_ok=True)

# def count_wednesdays(file_path):
#     count = 0
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             for line in file:
#                 date_str = line.strip()
#                 if not date_str:
#                     continue
#                 try:
#                     date = datetime.strptime(date_str, "%Y-%m-%d")
#                     if date.weekday() == 2:
#                         count += 1
#                 except ValueError:
#                     continue
#         return count
#     except FileNotFoundError:
#         return 0

# # Get the count of Wednesdays
# result = count_wednesdays(input_file)

# try:
#     # Open file in write mode and ensure it's correctly written
#     with open(output_file, "w", encoding="utf-8") as file:
#         file.write(f"{result}\n")
#         file.flush()  # Flush the buffer
#         os.fsync(file.fileno())  # Force the OS to write the file to disk before closing
#     print(f"Output successfully written to {output_file}")
# except Exception as e:
#     print(f"Error writing to {output_file}: {e}")


