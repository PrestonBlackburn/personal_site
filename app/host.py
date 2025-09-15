from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import markdown
from pathlib import Path
import logging
import os

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
    response = templates.TemplateResponse("pages/landing.html", context)

    return response


@app.get("/")
async def home(
    request: Request
) -> HTMLResponse:
    response = get_home_page(request, templates)
    return response

@app.get("/videos", response_class=HTMLResponse)
def serve_markdown_page(
    request: Request
)-> HTMLResponse:
    
    md_file = Path(f"app/static/content/videos/my-videos.md")
    if not md_file.exists():
        # can setup better 404 later
        return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)
    
    md_text = md_file.read_text(encoding="utf-8")
    html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])

    context = {"request": request, "content": html}
    response = templates.TemplateResponse("pages/videos.html", context)
    print(response)

    return response

@app.get("/projects", response_class=HTMLResponse)
def serve_markdown_page(
    request: Request
)-> HTMLResponse:
    
    md_file = Path(f"app/static/content/projects/projects-page.md")
    if not md_file.exists():
        # can setup better 404 later
        return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)
    
    md_text = md_file.read_text(encoding="utf-8")
    html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])

    context = {"request": request, "content": html}
    response = templates.TemplateResponse("pages/generic_md_page.html", context)
    print(response)

    return response

@app.get("/consulting", response_class=HTMLResponse)
def serve_markdown_page(
    request: Request
)-> HTMLResponse:
    
    md_file = Path(f"app/static/content/consulting/consulting-overview.md")
    if not md_file.exists():
        # can setup better 404 later
        return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)
    
    md_text = md_file.read_text(encoding="utf-8")
    html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])

    context = {"request": request, "content": html}
    response = templates.TemplateResponse("pages/generic_md_page.html", context)
    print(response)

    return response

@app.get("/tools", response_class=HTMLResponse)
def serve_markdown_page(
    request: Request
)-> HTMLResponse:
    
    md_file = Path(f"app/static/content/tools/my-tools.md")
    if not md_file.exists():
        # can setup better 404 later
        return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)
    
    md_text = md_file.read_text(encoding="utf-8")
    html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])

    context = {"request": request, "content": html}
    response = templates.TemplateResponse("pages/generic_md_page.html", context)
    print(response)

    return response

@app.get("/about", response_class=HTMLResponse)
def serve_markdown_page(
    request: Request
)-> HTMLResponse:
    
    md_file = Path(f"app/static/content/about/about.md")
    if not md_file.exists():
        # can setup better 404 later
        return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)
    
    md_text = md_file.read_text(encoding="utf-8")
    html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])

    context = {"request": request, "content": html}
    response = templates.TemplateResponse("pages/generic_md_page.html", context)
    print(response)

    return response

@app.get("/contact", response_class=HTMLResponse)
def serve_markdown_page(
    request: Request
)-> HTMLResponse:
    
    md_file = Path(f"app/static/content/contact/contact.md")
    if not md_file.exists():
        # can setup better 404 later
        return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)
    
    md_text = md_file.read_text(encoding="utf-8")
    html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])

    context = {"request": request, "content": html}
    response = templates.TemplateResponse("pages/generic_md_page.html", context)
    print(response)

    return response

@app.get("/blogs", response_class=HTMLResponse)
def serve_markdown_page(
    request: Request
)-> HTMLResponse:
    
    md_file = Path(f"app/static/content/blogs/summary.md")
    if not md_file.exists():
        # can setup better 404 later
        return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)
    
    md_text = md_file.read_text(encoding="utf-8")
    html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])

    context = {"request": request, "content": html}
    response = templates.TemplateResponse("pages/generic_md_page.html", context)
    print(response)

    return response

@app.get("/blog/{page_name}", response_class=HTMLResponse)
def serve_markdown_page(
    page_name:str, 
    request: Request
)-> HTMLResponse:
    
    md_file = Path(f"app/static/content/blogs/{page_name}.md")
    print(f'looking in {os.listdir(Path("app/static/content"))}')
    if not md_file.exists():
        # can setup better 404 later
        return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)
    
    md_text = md_file.read_text(encoding="utf-8")
    html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])

    context = {"request": request, "content": html}
    response = templates.TemplateResponse("pages/blog.html", context)
    print(response)

    return response


