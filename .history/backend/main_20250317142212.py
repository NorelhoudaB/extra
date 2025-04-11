import os
import shutil
import logging
from fastapi import FastAPI, UploadFile, HTTPException, File, Response
from fastapi.responses import JSONResponse,  FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from starlette.background import BackgroundTask
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

def clean():  
    tmpdir = Path("tmp")
    for file in tmpdir.iterdir():
        file.unlink()
    tmpdir.rmdir()
    
@app.get("/hello")
async def hello():
    return "heyy !!!!"


@app.post("/reduire")
async def optimise_images(file: UploadFile = File(...), del_jpeg: int = 0):
    try:
        logging.info(f"Début de l'optimisation des images {file.filename}")
        if not file:
            raise HTTPException(status_code=400, detail="Erreur : Veuillez choisir un fichier HTML")

        # ✅ Ensure tmp directory exists
        tmpdir = Path("tmp")
        if tmpdir.exists():
            shutil.rmtree(tmpdir)
        tmpdir.mkdir(exist_ok=True)

        file_path_html = tmpdir / file.filename

        # ✅ Read and write the file properly
        file_content = await file.read()
        if not file_content:
            raise HTTPException(status_code=400, detail="Erreur : Le fichier est vide ou corrompu")

        with file_path_html.open("wb") as f:
            f.write(file_content)

        # ✅ Ensure the file is saved properly
        if not file_path_html.exists():
            raise HTTPException(status_code=500, detail=f"Erreur : Le fichier {file_path_html} n'a pas été sauvegardé")

        print(f"✅ Fichier sauvegardé : {file_path_html}")

        # ✅ Process the file
        modified_html = RMF.process_images(file_path_html, del_jpeg)

        with file_path_html.open("w", encoding="utf-8") as f:
            f.write(modified_html)

        # ✅ Fix incorrect FileResponse usage
        return FileResponse(
            file_path_html,  # ✅ Now returning the correct file path
            media_type="application/xhtml+xml",
            background=BackgroundTask(clean),
        )

    except Exception as e:
        logging.error(f"Erreur lors de l'optimisation du fichier : {file.filename} - {e}")
        raise HTTPException(status_code=500, detail=f"Erreur : {str(e)}")


UPLOAD_DIR = "tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)  


@app.post("/fix-alt")
async def fix_alt(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    processed_file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
     print(f"File saved successfully~")

    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    img_pattern = re.compile(r'(<img\s+[^>]*?src="[^"]+")(?!\s+alt="image"\s)', re.IGNORECASE)
    count = 0

    def add_alt(match):
        nonlocal count
        count += 1
        return f'{match.group(1)} alt="image"'

    updated_content = img_pattern.sub(add_alt, html_content)
    print(f"Number of alt attributes added: {count}")

    with open(processed_file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    print("Updated file saved")

    download_url = f"/download/{file.filename}"
    print(f"Download link generated: {download_url}")

    return JSONResponse(content={"processed": updated_content, "download_url": download_url})

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

    return {"download_url": f"/download/{os.path.basename(html_path)}"}

@app.post("/change-thead")
async def change_thead(file: UploadFile):
    if not file.filename.endswith(('.html', '.xhtml')):
        raise HTTPException(400, "Invalid file type. Please upload an HTML or XHTML file.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    processed_filename = file.filename.replace(".xhtml", ".xhtml").replace(".html", ".html")
    processed_path = os.path.join(UPLOAD_DIR, processed_filename)

    print(f"Saving uploaded file: {file_path}")

    try:
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

        print(f"Processed file saved: {processed_path}")

        return {"download_url": f"/download/{processed_filename}"}

    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise HTTPException(500, f"An error occurred while processing the file: {str(e)}")
    
@app.get("/download/{filename}")
async def download_file(filename: str):
    processed_file_path = f"{UPLOAD_DIR}/{filename}"
    print(f"Serving file: {processed_file_path}")
    return FileResponse(processed_file_path, filename=f"{filename}", media_type="text/html")