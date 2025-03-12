import os
import shutil
import logging
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from starlette.background import BackgroundTask
import REMOVE_MERGE_FONTFACE as RMF

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
        os.makedirs(tmpdir, exist_ok=True)

        file_path_html = Path(tmpdir) / html_file.filename
        with file_path_html.open("wb") as file:
            file.write(await html_file.read())

        # DEBUG: Check if file exists
        if not file_path_html.exists():
            raise HTTPException(status_code=500, detail=f"Erreur : File {file_path_html} was not saved correctly")
        
        print(f"Saved file at: {file_path_html}")  # Debug log

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