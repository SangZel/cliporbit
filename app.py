
from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import uuid

app = FastAPI(
    title="ClipOrbit",
    description="The Internet's Best Live Moments",
    version="0.1.0"
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".mp4", ".mov", ".webm"}

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

@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    extension = Path(file.filename or "").suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only MP4, MOV and WEBM videos are allowed."
        )

    video_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{video_id}{extension}"

    size = 0
    max_size = 500 * 1024 * 1024

    try:
        with file_path.open("wb") as output:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)

                if size > max_size:
                    raise HTTPException(
                        status_code=413,
                        detail="Video exceeds 500 MB."
                    )

                output.write(chunk)
    except Exception:
        file_path.unlink(missing_ok=True)
        raise
    finally:
        await file.close()

    return {
        "status": "uploaded",
        "video_id": video_id,
        "filename": file.filename,
        "size_bytes": size
    }

