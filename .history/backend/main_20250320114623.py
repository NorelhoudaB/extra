import os
import shutil
import logging
from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import REMOVE_MERGE_FONTFACE as RMF
from lxml import etree
import re

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/hello")
async def hello():
    return "heyy !!!!"

@app.post("/reduire")
async def optimise_images(file: UploadFile = File(...), del_jpeg: int = 0):
    try:
        file_path_html = Path(UPLOAD_DIR) / file.filename
        file_content = await file.read()

        if not file_content:
            raise HTTPException(status_code=400, detail="Erreur : Le fichier est vide ou corrompu")

        with file_path_html.open("wb") as f:
            f.write(file_content)

        output_file_path = RMF.process_images(file_path_html, del_jpeg)

        if not output_file_path or not output_file_path.exists():
            raise HTTPException(status_code=500, detail="Erreur : Le fichier traité est introuvable")

        return FileResponse(output_file_path, filename=output_file_path.name, media_type="text/html")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur : {str(e)}")

@app.post("/fix-alt")
async def fix_alt(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    processed_file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    img_pattern = re.compile(r'(<img\s+[^>]*?src="[^"]+")(?!\s+alt="image"\s)', re.IGNORECASE)

    def add_alt(match):
        return f'{match.group(1)} alt="image"'

    updated_content = img_pattern.sub(add_alt, html_content)

    with open(processed_file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    return FileResponse(processed_file_path, filename=file.filename, media_type="text/html")

@app.post("/convert-xhtml")
async def convert_xhtml(file: UploadFile = File(...)):
    xhtml_path = os.path.join(UPLOAD_DIR, file.filename)
    html_path = os.path.join(UPLOAD_DIR, file.filename.replace(".xhtml", ".html"))       

    def xhtml_to_html(xhtml_file, html_file):
        parser = etree.XMLParser(recover=True)
        tree = etree.parse(xhtml_file, parser)

        for elem in tree.xpath('//@*'):
            if elem is None:
                elem.getparent().remove(elem)

        html_content = etree.tostring(tree, method="html", encoding="unicode")

        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

    with open(xhtml_path, "wb") as f:
        f.write(await file.read())

    xhtml_to_html(xhtml_path, html_path)

    return FileResponse(html_path, filename=os.path.basename(html_path), media_type="text/html")

@app.post("/change-thead")
async def change_thead(file: UploadFile):
    if not file.filename.endswith(('.html', '.xhtml')):
        raise HTTPException(400, "Invalid file type. Please upload an HTML or XHTML file.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    processed_filename = file.filename.replace(".xhtml", ".xhtml").replace(".html", ".html")
    processed_path = os.path.join(UPLOAD_DIR, processed_filename)

    content = (await file.read()).decode('utf-8')

    def replace_thead_if_no_tbody(table_content):
        if re.search(r'<thead\b', table_content) and not re.search(r'<tbody\b', table_content):
            return re.sub(r'</?thead\b', lambda x: x.group().replace('thead', 'tbody'), table_content)
        return table_content

    updated_content = re.sub(
        r'<table[^>]*>.*?</table>',
        lambda m: replace_thead_if_no_tbody(m.group()),
        content,
        flags=re.DOTALL
    )

    with open(processed_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    return FileResponse(processed_path, filename=processed_filename, media_type="text/html")

@app.post("/fix-space")
async def fix_space(file: UploadFile = File(...)):
    if not file.filename.endswith(('.html', '.xhtml')):
        raise HTTPException(400, "Invalid file type. Please upload an HTML or XHTML file.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    processed_filename = file.filename.replace(".xhtml", ".xhtml").replace(".html", ".html")
    processed_path = os.path.join(UPLOAD_DIR, processed_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("&#xa0;", " ")

    with open(processed_path, "w", encoding="utf-8") as f:
        f.write(content)

    return FileResponse(processed_path, filename=processed_filename, media_type="text/html")
