from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Header
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List
import os
import shutil
import logging
import hmac

_logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/images", tags=["images"])

IMAGE_DIR = Path(os.environ.get("IMAGE_STORAGE_PATH", "app/static/uploads"))
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_API_TOKEN = os.environ.get("IMAGE_API_TOKEN")

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}

def verify_token(authorization: str = Header(None)):
    if not IMAGE_API_TOKEN:
        raise HTTPException(status_code=500, detail="Server auth not configured")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or malformed Authorization header")
    token = authorization.removeprefix("Bearer ").strip()
    if not hmac.compare_digest(token, IMAGE_API_TOKEN):
        raise HTTPException(status_code=401, detail="Invalid token")
    return True

def _safe_filename(filename: str) -> str:
    # strip any path components to avoid path traversal (../../etc)
    name = Path(filename).name
    if not name or Path(name).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Invalid or disallowed filename: {filename}")
    return name


@router.get("", dependencies=[Depends(verify_token)])
async def list_images():
    files = sorted(
        IMAGE_DIR.glob("*"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    return {
        "images": [
            {
                "filename": f.name,
                "size_bytes": f.stat().st_size,
                "modified_at": f.stat().st_mtime,
            }
            for f in files
            if f.is_file()
        ]
    }


@router.post("", dependencies=[Depends(verify_token)])
async def upload_images(files: List[UploadFile] = File(...)):
    saved = []
    for upload in files:
        safe_name = _safe_filename(upload.filename)
        dest = IMAGE_DIR / safe_name
        with dest.open("wb") as out_file:
            shutil.copyfileobj(upload.file, out_file)
        _logger.info(f"Saved uploaded image to {dest}")
        saved.append(safe_name)
    return {"uploaded": saved}


@router.get("/{filename}", dependencies=[Depends(verify_token)])
async def download_image(filename: str):
    safe_name = _safe_filename(filename)
    file_path = IMAGE_DIR / safe_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(file_path)


@router.delete("/{filename}", dependencies=[Depends(verify_token)])
async def delete_image(filename: str):
    safe_name = _safe_filename(filename)
    file_path = IMAGE_DIR / safe_name
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    file_path.unlink()
    _logger.info(f"Deleted image {file_path}")
    return {"deleted": safe_name}