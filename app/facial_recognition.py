from fastapi import APIRouter, FastAPI, UploadFile, File, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dataclasses import dataclass
from contextlib import asynccontextmanager

from deepface import DeepFace
import numpy as np
import os
from pathlib import Path
import tempfile
import uuid
import datetime
import time
from collections import defaultdict
from typing import Dict, List, Optional
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
_logger = logging.getLogger(__name__)

API_PASSWORD = os.environ.get("FACE_API_PASSWORD", "")
RATE_LIMIT = 10 # per minute (window)
RATE_WINDOW = 60
request_history: defaultdict = defaultdict(list)

SHOPPERS_DIR = Path(f"app/static/face_db")
SIMILARITY_THRESHOLD = 0.4  # DeepFace cosine similarity: higher = more similar
TARGET_SIZE = (224, 224)  # Standard input size for face recognition models

face_encodings: Dict[str, np.ndarray] = {}
unmatched_faces: List[Dict] = []
current_shopper: str = None

def load_face_index():
    """Load face encodings from image files on disk at startup."""
    global face_encodings

    if not os.path.exists(SHOPPERS_DIR):
        os.makedirs(SHOPPERS_DIR, exist_ok=True)
        _logger.debug(f"Created empty shoppers directory: {SHOPPERS_DIR}")
        return

    for filename in os.listdir(SHOPPERS_DIR):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            filepath = os.path.join(SHOPPERS_DIR, filename)
            try:
                embedding = DeepFace.represent(
                    img_path=filepath,
                    model_name="Facenet512",
                    detector_backend="mtcnn",
                    align=True,
                    enforce_detection=False
                )
                if embedding:
                    shopper_category = os.path.splitext(filename)[0].replace("_", " ").title()
                    face_encodings[shopper_category] = np.array(embedding[0]["embedding"])
                    _logger.debug(f"  Indexed: {shopper_category}")
                else:
                    _logger.debug(f"  No face found in: {filename}")
            except Exception as e:
                _logger.debug(f"  Error loading {filename}: {e}")

    _logger.debug(f"Loaded {len(face_encodings)} face(s)")

@asynccontextmanager
async def startup_event(args):
    print("Loading face index...")
    load_face_index()
    print("Server ready.")
    yield

def _check_rate_limit(client_ip: str) -> bool:
    """Check if client has exceeded rate limit. Returns True if allowed."""
    now = time.time()
    window_start = now - RATE_WINDOW

    request_history[client_ip] = [
        ts for ts in request_history[client_ip] if ts > window_start
    ]

    if len(request_history[client_ip]) >= RATE_LIMIT:
        return False

    request_history[client_ip].append(now)
    return True


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))


def _track_unmatched(closest_match, closest_similarity):
    """Append an unmatched face entry and return its id."""
    uid = str(uuid.uuid4())
    unmatched_faces.append({
        "id": uid,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "closest_match": closest_match,
        "closest_similarity": closest_similarity,
    })
    return uid

def get_home_page(
        request: Request,
        templates: Jinja2Templates
) -> HTMLResponse:
    context = {"request": request}
    response = templates.TemplateResponse("pages/facial_recognition.html", context)
    return response


router = APIRouter(prefix="/face", lifespan=startup_event)
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def home(
    request: Request
) -> HTMLResponse:
    response = get_home_page(request, templates)
    return response

@router.post("/compare-face")
async def compare_face(
    request: Request,
    file: UploadFile = File(...),
    x_api_password: Optional[str] = Header(None)
):
    """
    Receive a captured face image, compare against the face index.
    If no match, track the face as unmatched.
    Requires password authentication via X-API-Password header.
    """
    global current_shopper
    client_ip = request.client.host if request.client else "unknown"

    _logger.debug(f"Got Password: {x_api_password}")
    _logger.debug(f"Expected Password: {API_PASSWORD}")
    if x_api_password != API_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid or missing password")

    if not _check_rate_limit(client_ip):
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    try:
        img_bytes = await file.read()

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp.write(img_bytes)
            tmp_path = tmp.name

        try:
            embedding = DeepFace.represent(
                img_path=tmp_path,
                model_name="Facenet512",
                detector_backend="mtcnn",
                align=True,
                enforce_detection=False
            )
        finally:
            os.unlink(tmp_path)

        if not embedding:
            raise HTTPException(status_code=400, detail="No face detected in image")

        captured_encoding = np.array(embedding[0]["embedding"])

        if not face_encodings:
            unmatched_id = _track_unmatched(None, 0.0)
            return {
                "match_found": False,
                "unmatched_id": unmatched_id,
                "closest_match": None,
                "closest_similarity": 0.0,
                "message": "No face indexed — face tracked as unmatched",
            }

        shopper_names = list(face_encodings.keys())
        similarities = []

        for name in shopper_names:
            sim = cosine_similarity(captured_encoding, face_encodings[name])
            similarities.append(sim)

        best_idx = int(np.argmax(similarities))
        best_similarity = similarities[best_idx]
        best_name = shopper_names[best_idx]
        current_shopper = best_name

        if best_similarity >= SIMILARITY_THRESHOLD:
            return {
                "match_found": True,
                "shopper": best_name,
                "distance": round(1.0 - best_similarity, 4),
                "confidence": best_similarity,
            }
        else:
            unmatched_id = _track_unmatched(best_name, best_similarity)
            return {
                "match_found": False,
                "unmatched_id": unmatched_id,
                "closest_match": best_name,
                "closest_similarity": round(best_similarity, 4),
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/get-results")
async def get_results():
    """Summary of current state."""
    return {
        "unmatched_faces_count": len(unmatched_faces),
        "shoppers_indexed": len(face_encodings),
        "shopper_categories": list(face_encodings.keys()),
    }


@router.get("/unmatched-faces")
async def get_unmatched_faces():
    """Return all tracked unmatched faces."""
    return {"unmatched_faces": unmatched_faces}


@router.get("/shoppers")
async def list_shoppers():
    """List indexed shopper categories."""
    return {"shoppers": list(face_encodings.keys())}


@router.get("/current-shopper")
async def list_current_shopper():
    """List the current/active shopper category to be used in eink display."""

    return {"shopper_category": str(current_shopper)}


@router.get("/reset-shopper")
async def reset_shopper():
    """Reset shopper"""
    global current_shopper 
    current_shopper = None

    return {"status": "success"}



