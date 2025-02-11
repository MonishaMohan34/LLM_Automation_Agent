

# /// script
# dependencies = [
#   "fastapi",
#   "uvicorn"
# ]
# ///

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def home():
    return {"message": "Hello, FastAPI with uv!"}

@app.get("/run")
def home():
    return {"message": "Hello, FastAPI with this is run!"}

# This ensures the app runs when executed with `uv run`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
