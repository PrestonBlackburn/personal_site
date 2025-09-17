from fastapi import FastAPI, Depends, HTTPException, Response, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

import markdown
from pathlib import Path
import logging
import os
from datetime import datetime

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
    context = {"request": request, "landing_page": True}
    # later - contextually show landing page stuff
    response = templates.TemplateResponse("pages/landing.html", context)

    return response


@app.get("/")
async def home(
    request: Request
) -> HTMLResponse:
    response = get_home_page(request, templates)
    return response


# For generic pages (just md serving)
custom_md_pages = {
    "videos": Path(f"app/static/content/videos/my-videos.md"),
    "projects": Path(f"app/static/content/projects/projects-page.md"),
    "consulting": Path(f"app/static/content/consulting/consulting-overview.md"),
    "tools": Path(f"app/static/content/tools/my-tools.md"),
    "about": Path(f"app/static/content/about/about.md"),
    "contact": Path(f"app/static/content/contact/contact.md"),
    # "blogs": Path(f"app/static/content/blogs/summary.md"),
}

def generic_markdown_page_generator(content_path:Path):
    def serve_markdown_page(
        request: Request,
    )-> HTMLResponse:
        
        if not content_path.exists():
            # can setup better 404 later
            return HTMLResponse("<h1>404 Not Found</h1>", status_code=404)
        
        md_text = content_path.read_text(encoding="utf-8")
        html = markdown.markdown(md_text, extensions=['fenced_code', 'codehilite'])

        context = {"request": request, "content": html, "landing_page": False}
        response = templates.TemplateResponse("pages/generic_md_page.html", context)
        print(response)

        return response
    return serve_markdown_page

for page_route, content_path in custom_md_pages.items():
    serve_md_page = generic_markdown_page_generator(content_path)
    app.add_api_route(f"/{page_route}", serve_md_page, response_class=HTMLResponse, methods=["GET"])



def get_blog_metadata(blog_dir:Path = Path("app/static/content/blogs")):
    blog_files = [f for f in blog_dir.glob("*.md") if f.is_file() and f.name != "summary.md"]
    metadata = []
    for blog_file in blog_files:
        # Simple metadata extraction from filename, can be extended to read front-matter if needed
        blog_data = {}
        with open(blog_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            title = lines[0].strip()
            date = None
            for line in lines[1:]:
                if "," in line and line[0].isalpha():
                    date = line.strip()
                    break
            thumbnail = None
            for line in lines:
                if line.startswith("![") and "(" in line and ")" in line:
                    thumbnail = line.split("(", 1)[1].rsplit(")", 1)[0].strip()
                    break

            blog_data.update({"title": title, "date": date, "thumbnail_image": thumbnail, "slug": blog_file.stem})
        metadata.append(blog_data)

        # sort metadta by date (newest first)
        metadata = sorted(metadata, key=lambda x: datetime.strptime(x['date'], "%b %d, %Y"), reverse=True)
    return metadata    

@app.get("/blogs", response_class=HTMLResponse)
def serve_blogs_landing(
    request: Request
)-> HTMLResponse:
    
    blog_metadata = get_blog_metadata()

    context = {"request": request, "blogs_metadata": blog_metadata}
    response = templates.TemplateResponse("pages/blogs.html", context)
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


@app.get("/api/v1/pages")
def list_pages():
    return {"pages": list(custom_md_pages.keys())}

@app.get("/api/v1/blogs")
def list_blogs():
    blog_dir = Path("app/static/content/blogs")
    blog_files = [f.stem for f in blog_dir.glob("*.md") if f.is_file() and f.name != "summary.md"]
    return {"blogs": blog_files}

@app.get("/api/v1/blogs/metadata")
def blogs_metadata():
    metadata = get_blog_metadata()
    return {"blogs": metadata}