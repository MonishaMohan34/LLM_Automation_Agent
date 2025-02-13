FROM python:3.12-slim-bookworm

# Install dependencies required for UV and Python virtual environments
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates python3-venv && \
    rm -rf /var/lib/apt/lists/*

# Download and install UV
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure UV is in the PATH
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install required Python packages (FastAPI, Uvicorn, Requests)
RUN pip install --no-cache-dir fastapi uvicorn requests

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI server
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

CMD ["uv","run","app.py"]
