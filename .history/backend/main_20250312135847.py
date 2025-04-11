import os
import shutil
import logging
from fastapi import FastAPI, UploadFile, HTTPException, File, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from starlette.background import BackgroundTask
import REMOVE_MERGE_FONTFACE as RMF

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
    if os.path.exists("tmp"):
        shutil.rmtree("tmp")

@app.get("/hello")
async def hello():
    return "HELLO WORLD"


@app.post("/reduire")
async def optimise_images(html_file: UploadFile, del_jpeg: int = 0):
    try:
        if not html_file:
            raise HTTPException(status_code=400, detail="Erreur : Veuillez choisir un fichier HTML")
        
        tmpdir = "tmp"
        os.makedirs(tmpdir, exist_ok=True)  # Ensure tmp directory exists

        file_path_html = Path(tmpdir) / html_file.filename
        with file_path_html.open("wb") as file:
            file.write(await html_file.read())

        # Debugging: Check if the file actually exists
        if not file_path_html.exists():
            raise HTTPException(status_code=500, detail=f"Erreur : File {file_path_html} was not saved correctly")

        print(f"✅ File saved at: {file_path_html}")

        # Debugging: Print before processing the file
        print(f"📌 Sending file to RMF.process_images: {file_path_html}")

        if not file_path_html.exists():
          logging.error(f"File does not exist: {file_path_html}")
          raise HTTPException(status_code=500, detail=f"Erreur : File {file_path_html} not found before processing")

        modified_html = RMF.process_images(file_path_html, del_jpeg)


        with file_path_html.open("w", encoding="utf-8") as f:
            f.write(modified_html)

        return FileResponse(
            file_path_html,
            media_type="application/xhtml+xml",
            background=BackgroundTask(clean),
        )

    except Exception as e:
        logging.error(f"Erreur lors de l'optimisation du fichier : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur : {e}")


def fix_alt(html_content: str) -> str:
    # Regex pour détecter les balises <img> avec src mais sans alt="image"
    img_pattern = re.compile(r'(<img\s+[^>]*?src="[^"]+")(?!\s+alt="image")', re.IGNORECASE)
    count = 0  # Compteur d'ajouts
    # Fonction pour ajouter alt="image" immédiatement après src
    def add_alt(match):
        nonlocal count
        count += 1
        return f'{match.group(1)} alt="image"'
    # Remplacement
    updated_content = img_pattern.sub(add_alt, html_content)
    print(f'Nombre de balises alt ajoutées : {count}')
    return updated_content
 
@app.post("/fix-alt")
async def fix_alt_endpoint(file: UploadFile = File(...)):
    content = await file.read()
    html_content = content.decode("utf-8")
    updated_content = fix_alt(html_content)
    return Response(content=updated_content, media_type=file.content_type)