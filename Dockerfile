FROM python:3.12-slim-bookworm

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Install Tesseract OCR and language data
RUN apt-get update && apt-get install -y tesseract-ocr && apt-get clean

RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-deu tesseract-ocr-fra && apt-get clean


# Download and install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

# Set the working directory
WORKDIR /app

# Create a virtual environment for uv
RUN uv venv /app/.venv

# Install Python dependencies inside uv's virtual environment
RUN uv pip install fastapi uvicorn requests pillow faker scikit-learn numpy pandas scipy python-dateutil pytesseract


# Ensure the virtual environment is activated
ENV UV_VENV="/app/.venv"


# Copy application files
COPY app1.py evaluate.py datagen.py /app/

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI using uv
CMD ["uv", "run", "app1.py"]



