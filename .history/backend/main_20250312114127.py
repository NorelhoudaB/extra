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

async def optimise_images(
    html_file: UploadFile = UploadFile(...),
    del_jpeg: int = 0,
):
    try:
        logging.info(f"Début de l'optimisation des images {html_file.filename}")
        if not html_file: raise HTTPException(status_code=500, detail=f"Erreur : Veuillez choisir les fichier HTML")
        tmpdir = "tmp"
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        os.mkdir(tmpdir)
        file_path_html = Path(tmpdir)/html_file.filename
        with file_path_html.open("wb") as file:
            file.write(await html_file.read())
        with open(file_path_html, 'r', encoding='utf-8') as file:
            html_content = file.read()
        modified_html = RMF.process_images(file_path_html,del_jpeg)
        with open(file_path_html, "w", encoding="utf-8") as f:
            f.write(modified_html)

        #return FileResponse(file_path_html)
        return FileResponse(
            modified_html,
            media_type="application/xhtml+xml",
            background=BackgroundTask(clean),
        )

    except Exception as e:
        logging.error(
            f"Erreur lors de l'optimisation du fichier : {html_file.filename} - {e}"
        )
        raise HTTPException(status_code=500, detail=f"Erreur : {e}")
