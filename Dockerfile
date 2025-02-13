FROM python:3.12-slim-bookworm

# Install required dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download and install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN uv pip install fastapi uvicorn requests

# Copy application files
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run the FastAPI application

# Start FastAPI server
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

CMD ["uv","run","python","app.py"]
