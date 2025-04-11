
import os
import shutil
import logging
import sys
import pdb
from fastapi import Security, Depends, FastAPI, UploadFile, Form, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from zipfile import ZipFile
import zipfile
from pathlib import Path
from starlette.background import BackgroundTask
from io import StringIO
#from OPTIMISE_WORD import Process_Word
#from OPTIMISE_WORD_TABLE import Process_Word_Table
#from WORD_TO_HTML import Word_To_HTML
import app.REMOVE_MERGE_FONTFACE as RMF
import pdb
import debugpy
from tempfile import NamedTemporaryFile
import re
from lxml import etree
import tempfile


app = FastAPI()

def clean():
    if os.path.exists("tmp"):
        shutil.rmtree("tmp")
    if os.path.exists("tmp_word"):
        shutil.rmtree("tmp_word")

@app.get("/hello")
async def hello():
    return "HELLO WORLD"

@app.post("/optimise/images")
async def optimise_images(
    html_file: UploadFile = UploadFile(...),
    # api_key: APIKey = Depends(get_api_key),
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
