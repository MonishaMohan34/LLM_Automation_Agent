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


# import pytesseract
# from PIL import Image
# import re

# # Path to input image and output text file
# input_image = r"C:/Users/monis/data/credit_card.png" 
# output_file = r"C:/Users/monis/data/credit_card.png" 





# # Load the image
# image = Image.open(input_image)

# # Perform OCR
# extracted_text = pytesseract.image_to_string(image, config='--psm 6')

# # Extract only digits (credit card number)
# credit_card_number = "".join(re.findall(r'\d+', extracted_text))

# # Save to output file
# if credit_card_number:
#     with open(output_file, "w") as f:
#         f.write(credit_card_number)
#     print(f"Extracted credit card number saved to {output_file}.")
# else:
#     print("No credit card number found.")



# import os
# import numpy as np
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity

# input_file = "./data/comments.txt"
# output_file = "./data/comments-similar.txt"
# # input_file = "C:/Users/monis/data/comments.txt"
# # output_file = "C:/Users/monis/data/comments-similar.txt"
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
#     # Load a pre-trained sentence transformer model
#     model = SentenceTransformer('all-MiniLM-L6-v2')  # Efficient and accurate

#     # Compute embeddings
#     embeddings = model.encode(comments, normalize_embeddings=True)

#     # Compute cosine similarity
#     cosine_similarities = cosine_similarity(embeddings)

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


# import re
# import os

# # Define input and output file paths
# input_file = "C:/Users/monis/data/email.txt"
# output_file = "C:/Users/monis/data/email-details.txt"

# # Ensure the output directory exists
# os.makedirs(os.path.dirname(output_file), exist_ok=True)

# # Function to extract email addresses from different fields
# def extract_emails(content, field):
#     pattern = rf"^{field}:\s+(.+)$"
#     match = re.search(pattern, content, re.MULTILINE)
#     if not match:
#         return []
    
#     # Extract email addresses from the matched line
#     email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
#     emails = re.findall(email_pattern, match.group(1))
#     return emails

# # Read the email content
# try:
#     with open(input_file, "r", encoding="utf-8") as file:
#         content = file.read()
# except FileNotFoundError:
#     print(f"Error: {input_file} not found.")
#     exit(1)

# # Extract different types of email addresses
# sender_email = extract_emails(content, "From")
# receiver_emails = extract_emails(content, "To")
# cc_emails = extract_emails(content, "Cc")

# # Debugging Output
# print(f"Sender Email: {sender_email}")
# print(f"Receiver Emails: {receiver_emails}")
# print(f"CC Emails: {cc_emails}")

# # Save the extracted emails to a file
# with open(output_file, "w", encoding="utf-8") as file:
#     file.write(f"Sender: {', '.join(sender_email)}\n")
#     file.write(f"To: {', '.join(receiver_emails)}\n")
#     file.write(f"Cc: {', '.join(cc_emails)}\n")

# print(f"Email details extracted and saved to {output_file}")





# from datetime import datetime
# from dateutil.parser import parse

# input_file = "./data/dates.txt"
# output_file = "./data/dates-wednesdays.txt"

# # List of date formats to check explicitly
# date_formats = [
#     "%Y-%m-%d",
#     "%d-%b-%Y",
#     "%m/%d/%Y",
#     "%d/%m/%Y",
#     "%B %d, %Y",
#     "%Y/%m/%d %H:%M:%S",
#     "%Y-%m-%d %H:%M:%S",
#     "%d-%b-%Y %H:%M:%S",
#     "%b %d, %Y"
# ]

# # Function to parse a date string
# def parse_date(date_str):
#     date_str = date_str.strip()
#     if not date_str:
#         return None
#     # Try all known formats first
#     for fmt in date_formats:
#         try:
#             return datetime.strptime(date_str, fmt)
#         except ValueError:
#             continue
#     # If no format matched, try the generic parser
#     try:
#         return parse(date_str, fuzzy=True)
#     except ValueError:
#         return None

# # Function to count Wednesdays in the provided date file
# def count_wednesdays(file_path):
#     count = 0
#     try:
#         with open(file_path, "r", encoding="utf-8") as file:
#             for line in file:
#                 date = parse_date(line)
#                 if date and date.weekday() == 2:  # 2 = Wednesday
#                     count += 1
#         return count
#     except FileNotFoundError:
#         return 0

# # Get the count of Wednesdays
# result = count_wednesdays(input_file)

# # Write the result to the output file
# try:
#     with open(output_file, "w", encoding="utf-8") as file:
#         file.write(f"{result}\n")
# except Exception as e:
#     print(f"Error writing to {output_file}: {e}")



