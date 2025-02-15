from pathlib import Path

# Define the input and output paths
logs_dir = Path('/data/logs/')
output_file = Path('/data/logs-recent.txt')

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