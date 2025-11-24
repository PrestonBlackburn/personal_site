from pathlib import Path
# custom pages - 
from host import custom_md_pages
import xml.etree.ElementTree as ET
from datetime import datetime

def get_blog_urls():
    # blogs path - 
    # root/blog/{page_name}
    blog_dir = Path("app/static/content/blogs")
    blog_files = [f for f in blog_dir.glob("*.md") if f.is_file() and f.name != "summary.md"]
    urls = []
    for blog_file in blog_files:
        page_name = blog_file.stem
        # clearn urls (to match frontend routing)
        page_name = page_name.lower().replace("'", "").replace(" ", "-")
        url = f"https://prestonblackburn.com/blog/{page_name}"
        urls.append(url)
    return urls


def get_custom_page_urls():
    base_url = "https://prestonblackburn.com/"
    urls = []
    for page_route in custom_md_pages.keys():
        url = f"{base_url}{page_route}"
        urls.append(url)
    return urls

def create_url_xml_element(root: ET.Element, url:str, changefreq="monthly", priority="0.5", lastmod=None):
    url_element = ET.SubElement(root, "url")
    loc = ET.SubElement(url_element, "loc")
    loc.text = url
    change_freq = ET.SubElement(url_element, "changefreq")
    change_freq.text = changefreq
    priority_el = ET.SubElement(url_element, "priority")
    priority_el.text = priority
    if lastmod:
        last_mod = ET.SubElement(url_element, "lastmod")
        last_mod.text = lastmod
    return url_element

def generate_sitemap():

    root = ET.Element("urlset")
    root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    blog_urls = get_blog_urls()
    custom_page_urls = get_custom_page_urls()
    for url in blog_urls:
        last_mod_date = datetime.now().strftime("%Y-%m-%d")
        create_url_xml_element(root, url, changefreq="monthly", priority="0.8", lastmod=last_mod_date)
    for url in custom_page_urls:
        create_url_xml_element(root, url, changefreq="yearly", priority="0.6")
    
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    tree.write(Path("app/static/metadata/sitemap.xml"), encoding="utf-8", xml_declaration=True, method="xml")



if __name__ == "__main__":
    generate_sitemap()