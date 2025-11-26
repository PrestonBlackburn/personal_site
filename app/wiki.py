from fastapi import APIRouter, Depends, HTTPException, Response, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from dataclasses import dataclass
import json
import markdown
from pathlib import Path
import logging
import os
from datetime import datetime
import random
from rapidfuzz import process, fuzz

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
_logger = logging.getLogger(__name__)

router = APIRouter(prefix="/wiki")
templates = Jinja2Templates(directory="app/templates")


# ------ Wiki Utils -------

def clean_topic_name(topic:str):
    return topic.replace(" ", "_").replace("-", "_").replace(",", "_").replace("/", "_")

def get_cleaned_key_dict(topic_dict: str):
    cleaned_dict = {}
    for key, value in topic_dict.items():
        cleaned_dict.update({clean_topic_name(key): value})

    return cleaned_dict

@dataclass
class BookReference:
    authors:str
    source_date:str
    source_name:str
    source_link:str
    publisher:str
    pages:str
    isbn_number:str

    def to_string(self):
        if self.source_date != "":
            date = f" ({self.source_date})."
        else:
            date = "."
        if self.publisher != "":
            publisher = f'" {self.publisher}".'
        else:
            publisher = ""
        if self.source_name != "":
            source = f"<i>{self.source_name}</i>."
        else:
            source = ""
        if self.pages != "":
            pages = f"{self.pages}."
        else:
            pages = ""
        if self.isbn_number != "":
            isbn = f"""<a href="/wiki/ISBN_{self.isbn_number}" class="mw-redirect" title="ISBN {self.isbn_number}">ISBN</a>&nbsp;<a href="/wiki/Special:BookSources/{self.isbn_number}" title="Special:BookSources/{self.isbn_number}"><bdi>{self.isbn_number}</bdi>
            </a>."""
        else:
            isbn = ""

        ref_html = f"""<span class="reference-text">
        <link rel="mw-deduplicated-inline-style" href="mw-data:TemplateStyles:r1238218222">
        <cite id="{self.authors.lower().replace(" ", "_")}" class="citation book cs1">
        {self.authors}{date}{publisher} 
            {source} {pages} 
            {isbn}
            </cite>
        </span>"""
        return ref_html
    
@dataclass
class ArticleReference:
    reference_author:str
    reference_title:str
    reference_link:str
    reference_source:str
    reference_date:str
    archive_link:str
    archive_date:str
    retreived_date:str

    def to_string(self):

        if self.reference_date != "":
            ref_date = f"({self.reference_date})"
        else:
            ref_date = ""
        
        if self.reference_author != "":
            authors = f"{self.reference_author} {ref_date}."
        else:
            authors = ""

        if self.archive_date != "":
            archive = f"""<a rel="nofollow" class="external text" href="{self.reference_link}">Archived</a> from the original on {self.archive_date}."""
        else:
            archive = ""
        if self.retreived_date != "":
            ret_date = f"""<span class="reference-accessdate">
                Retrieved <span class="nowrap">{self.retreived_date}</span></span>."""
        else:
            ret_date = ""


        ref_html = f"""
            <span class="reference-text">
            <link rel="mw-deduplicated-inline-style" href="mw-data:TemplateStyles:r1238218222">
            <cite id="{self.reference_title.lower().replace(" ", "_")}" class="citation web cs1">
                {authors}
            <a rel="nofollow" class="external text" href="{self.reference_link}">"{self.reference_title}"</a>{archive} {ret_date}
            </cite>
            </span>
        """

        return ref_html
    
@dataclass
class SectionData:
    section_title: str
    section_content: str
    section_image_link: str # maybe optional

    # def merge_links(self, refs:list):
    #     self.section_content.split(".")
    #     # randomly add ref links in
    #     self.section_content = section_content_with_refs
    #     return
    # """A diagram representation of {topic} and {section}"""

    def get_section_image_path(self, topic:str, base_path:str):

        topic_path = clean_topic_name(topic)
        section_path = clean_topic_name(self.section_title)

        img_path = f"{base_path}/{topic_path}/{section_path}.webp"
        self.section_image_link = img_path

        return self
    

@dataclass
class PersonalSection:
    section_title: str
    section_content: str
    section_image_link:str

def get_topics() -> list:
    with open("app/static/content/generated/generated_topics.txt", "r") as f:
        topics = f.read()
    topics = topics.split("\n")
    return topics

def get_sections_for_topic(topic:str, base_path: str = "") -> list[SectionData]:
    with open("app/static/content/generated/section_bodies.json", "r") as f:
        topic_sections = json.loads(f.read())

    topic_sections = get_cleaned_key_dict(topic_sections)
    sections = topic_sections[topic]
    topic_path = clean_topic_name(topic)
    data = []
    for section_title, section_content in sections.items():
        section_path = clean_topic_name(section_title)
        section_data = SectionData(
            section_title = section_title,
            section_content =  markdown.markdown(section_content, extensions=['fenced_code', 'codehilite']),
            section_image_link = f"{base_path}/{topic_path}/{section_path}.webp"
        )
        data.append(section_data)
    return data

def get_personal_section_for_topic(topic:str) -> PersonalSection:
    # may add in later...
    with open("app/static/content/generated/related_to_me.json", "r") as f:
        topic_sections = json.loads(f.read())

    topic_sections = get_cleaned_key_dict(topic_sections)
    
    personal_section = PersonalSection(
        section_title = "Related To Preston Blackburn",
        section_content = markdown.markdown(topic_sections[topic], extensions=['fenced_code', 'codehilite']),
        section_image_link = "/static/img/wiki/icons/placeholder_image.jpg"
    )
    return personal_section

def get_book_references_for_topic(topic:str) -> list[BookReference]:
    with open("app/static/content/generated/book_refs.json", "r") as f:
        refs = json.loads(f.read())
    
    refs = get_cleaned_key_dict(refs)

    filtered_refs = refs[topic]
    book_refs = []
    for ref in filtered_refs:
        book_ref = BookReference(**ref)
        book_refs.append(book_ref)
    return book_refs

def get_article_references_for_topic(topic:str) -> list[ArticleReference]:
    with open("app/static/content/generated/article_refs.json", "r") as f:
        refs = json.loads(f.read())
    
    refs = get_cleaned_key_dict(refs)

    filtered_refs = refs[topic]
    article_refs = []
    for ref in filtered_refs:
        article_ref = ArticleReference(**ref)
        article_refs.append(article_ref)

    return article_refs

def get_articles_for_topic(topic:str) -> list[str]:

    book_refs = get_book_references_for_topic(topic)
    article_refs = get_article_references_for_topic(topic)

    refs = []
    for i in range(0, max(len(book_refs), len(article_refs))):
        if len(book_refs) > i:
            refs.append(book_refs[i].to_string())
        if len(article_refs) > i:
            refs.append(article_refs[i].to_string())   
    return refs

TOKEN = "M-A-C-G-U-F-F-I-N"

def get_random_hitchcock_fact():
    with open("app/static/content/facts/alfred_hitchcock.json", "r") as f:
        facts = json.loads(f.read())
    facts_list = facts["facts"]
    idx = random.randint(0, len(facts_list)-1)
    return facts_list[idx]

def get_token_content():
    fact = get_random_hitchcock_fact()
    token_content = f"&lt;{TOKEN}&gt; {fact}"
    token_content_js = f"<{TOKEN}> {fact}"
    html_content = f"""<p class="token-text">{token_content}</p>"""
    js_content = f"""<script type="application/ld+json">{{"fact": "{token_content_js}"}}</script>"""

    return html_content, js_content


# ------------ Endpoints ------------

def get_home_page(
        request: Request,
        templates: Jinja2Templates
) -> HTMLResponse:
    context = {"request": request}
    response = templates.TemplateResponse("pages/wiki_search.html", context)
    return response

def get_wiki_page(
    request: Request, 
    templates: Jinja2Templates, 
    topic: str
) -> HTMLResponse:
    
    base_img_path = "/static/img/generated"
    # topic = "Kubernetes for ML Infrastructure"
    sections = get_sections_for_topic(topic, base_path = base_img_path)
    personal_section = get_personal_section_for_topic(topic)
    see_also = get_topics()
    see_also_limited = [see_also[random.randint(1, len(see_also))] for _ in range(0, random.randint(3, 8))]
    see_also_with_links = [(topic, f"/wiki/{clean_topic_name(topic)}") for topic in see_also_limited]
    refs = get_articles_for_topic(topic)
    sections = [section.get_section_image_path(topic, base_img_path) for section in sections]
    token_html_content, token_js_content = get_token_content()
    sections[-1].section_content = f"""{sections[-1].section_content} {token_html_content}"""

    context = {
        "request": request, 
        "landing_page": True,
        # we have a lot of data to provide...
        "title": topic.replace("_", " "),
        "overview_image_link": sections[0].section_image_link,
        "overview_image_caption": f"""A diagram representation of {topic} and {sections[0].section_title}""",
        "overview_content": sections[0].section_content,
        "section_data": sections[1:],
        "personal_section": personal_section,
        "see_also": see_also_with_links,
        "refs": refs,
        "metadata": token_js_content
    }
    # later - contextually show landing page stuff
    response = templates.TemplateResponse("pages/wiki.html", context)

    return response

def get_searched_wiki_pages(
    request: Request, 
    templates: Jinja2Templates, 
    search_text: str
):
    base_img_path = "/static/img/generated"
    all_topics = get_topics()
    _logger.info(f"Searching For: {search_text}")
    similar_topics = process.extract(
        search_text, 
        all_topics, 
        scorer=fuzz.WRatio, 
        limit=10
    )
    _logger.info(f"Similar Topics: {similar_topics}")
    thumbnails = []
    for topic, score, rank in similar_topics:
        sections = get_sections_for_topic(clean_topic_name(topic), base_path = base_img_path)
        thumbnail = {
            "src": f"{clean_topic_name(topic)}",
            "title": topic,
            "image": sections[0].section_image_link,
            "overview": sections[0].section_content[0:100] + "..."
        }
        thumbnails.append(thumbnail)

    context = {
        "request": request, 
        "thumbnails": thumbnails
    }
    response = templates.TemplateResponse("components/wiki/thumbnails.html", context)
    return response

@router.get("/")
async def home(
    request: Request
) -> HTMLResponse:
    response = get_home_page(request, templates)
    return response

@router.get("/{topic}")
async def get_page(
    request: Request,
    topic: str
) -> HTMLResponse:
    response = get_wiki_page(request, templates, topic)
    return response

@router.post("/search")
async def search(
    request: Request,
    search_text: str = Form(...)
) -> HTMLResponse:
    response = get_searched_wiki_pages(request, templates, search_text)

    return response