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
    return "heyy !!!!"


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


UPLOAD_DIR = "tmp"
os.makedirs(UPLOAD_DIR, exist_ok=True)  


@app.post("/fix-alt")
async def fix_alt(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"
    processed_file_path = f"{UPLOAD_DIR}/processed_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    img_pattern = re.compile(r'(<img\s+[^>]*?src="[^"]+")(?!\s+alt="image")', re.IGNORECASE)
    
    def add_alt(match):
        return f'{match.group(1)} alt="image"'
    
    updated_content = img_pattern.sub(add_alt, html_content)

    with open(processed_file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    file_response = FileResponse(processed_file_path, filename=f"processed_{file.filename}", media_type="text/html")

    return Response(content=updated_content, media_type=file.content_type, headers={"Content-Disposition": f'attachment; filename="processed_{file.filename}"'})