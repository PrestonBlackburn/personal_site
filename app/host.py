from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("uvicorn").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.error").setLevel(logging.DEBUG)
logging.getLogger("uvicorn.access").setLevel(logging.INFO)
logging.getLogger("pat").setLevel(logging.DEBUG)
logging.getLogger("rubric_core").setLevel(logging.INFO)

app = FastAPI()

# TODO - add restrictions when in prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allows all origins (use specific origins in production for better security)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

templates = Jinja2Templates(directory="app/templates")

# static files (nees to be called before the router for pathing)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


def get_home_page(
    request: Request, 
    templates: Jinja2Templates, 
) -> HTMLResponse:
    context = {"request": request}
    # later - contextually show landing page stuff
    response = templates.TemplateResponse("x_term_test.html", context)

    return response


@app.get("/")
async def home(
    request: Request
) -> HTMLResponse:
    response = get_home_page(request, templates)
    return response
