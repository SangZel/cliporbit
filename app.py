
from fastapi import FastAPI

app = FastAPI(
    title="ClipOrbit",
    description="The Internet's Best Live Moments",
    version="0.1.0"
)

@app.get("/")
def home():
    return {
        "project": "ClipOrbit",
        "status": "running",
        "message": "Welcome to ClipOrbit!"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
  
