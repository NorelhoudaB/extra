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
import REMOVE_MERGE_FONTFACE as RMF
import pdb
import debugpy
from tempfile import NamedTemporaryFile
import re
from lxml import etree
import tempfile



origins = ["*"]

API_KEY = "455514d9-183a-4f8f-8947-f85b6e3b3cca"
API_KEY_NAME = "token"
COOKIE_DOMAIN = "optimise.api"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
    api_key_cookie: str = Security(api_key_cookie),
):
    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    raise HTTPException(status_code=403, detail="Invalid API key")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    filename="api.log",  # Specify the log file name and location
    level=logging.INFO,  # Set the logging level (e.g., INFO, DEBUG)
    format="%(asctime)s [%(levelname)s]: %(message)s",  # Define the log message format
    datefmt="%Y-%m-%d %H:%M:%S",  # Define the date and time format
)
logging.info("Nouveau fichier log")


def clean():
    if os.path.exists("tmp"):
        shutil.rmtree("tmp")
    if os.path.exists("tmp_word"):
        shutil.rmtree("tmp_word")

@app.get("/hello")
async def hello():
    return "HELLO WORLD"


# except Exception as e:
#     if not folder.filename:
#         logging.error(f"Erreur fichier vide")
#         raise HTTPException(status_code=500, detail=f"Erreur : fichier vide")
#     else:
#         logging.error(
#             f"Erreur lors de l'optimisation du fichier : {folder.filename} - {e}"
#         )
#         raise HTTPException(status_code=500, detail=f"Erreur : {e}")


"""@app.post("/optimise/word")
async def optimise_word(
    html_file: UploadFile = UploadFile(...),
    # api_key: APIKey = Depends(get_api_key),
):
    try:
        logging.info(f"Début de l'optimisation du fichier : {html_file.filename}")
        tmpdir = "tmp_word"
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)

        os.mkdir(tmpdir)

        file_path = Path(tmpdir) / html_file.filename
        with file_path.open("wb") as buffer:
            buffer.write(await html_file.read())

        extracted_folder = os.path.join(tmpdir, "extracted")
        os.makedirs(extracted_folder)

        with ZipFile(file_path) as zip:
            zip.extractall(extracted_folder)
        xhtml_output = Process_Word(extracted_folder)

        logging.info(f"Optimisation réussie du fichier : {html_file.filename}")

        return FileResponse(
            xhtml_output,
            media_type="application/xhtml+xml",
            background=BackgroundTask(clean),
        )
    except Exception as e:
        logging.error(
            f"Erreur lors de l'optimisation du fichier : {html_file.filename} - {e}"
        )
        raise HTTPException(status_code=500, detail=f"Erreur : {e}")"""


"""@app.post("/optimise/word_table")
async def optimise_word_table(
    word_file: UploadFile = UploadFile(...),
    # api_key: APIKey = Depends(get_api_key),
):
    try:
        logging.info(f"Début de l'optimisation du fichier : {word_file.filename}")
        tmpdir = "tmp_word_table"
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)

        os.mkdir(tmpdir)

        file_path = Path(tmpdir) / word_file.filename
        with file_path.open("wb") as buffer:
            buffer.write(await word_file.read())

        extracted_folder = os.path.join(tmpdir, "extracted")
        os.makedirs(extracted_folder)

        with ZipFile(file_path) as zip:
            zip.extractall(extracted_folder)
        word_output = Process_Word_Table((extracted_folder))

        logging.info(f"Optimisation réussie du fichier : {word_file.filename}")

        return FileResponse(
            word_output,
            media_type="application/xhtml+xml",
            background=BackgroundTask(clean),
        )
    except Exception as e:
        logging.error(
            f"Erreur lors de l'optimisation du fichier : {word_file.filename} - {e}"
        )
        raise HTTPException(status_code=500, detail=f"Erreur : {e}")"""


"""@app.post("/optimise/word_to_html")
async def process_files(
    zip_file: UploadFile = UploadFile(...),
    # api_key: APIKey = Depends(get_api_key),
):
    try:
        logging.info(f"Début de l'optimisation du fichier : {zip_file.filename}")

        tmpdir = "tmp_word"
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        os.mkdir(tmpdir)
        # get file path
        file_path = Path(tmpdir) / zip_file.filename
        #save file on tmp diroctory
        with file_path.open("wb") as file:
            file.write(await zip_file.read())
        # extract all file
        extracted_folder = os.path.join(tmpdir, "extracted")
        os.makedirs(extracted_folder)

        with ZipFile(file_path) as zip_ref:
            zip_ref.extractall(extracted_folder)
        # get name folder unziped
        folder_name = str(zip_file.filename).replace('.zip', '')
        # get full path folder unziped
        path_folder_zip = f"{extracted_folder}/{folder_name}"
        # Call your function to process the extracted folder
        xhtml_output = Word_To_HTML(path_folder_zip)

        logging.info(f"Optimisation réussie du fichier : {zip_file.filename}")

        logging.info("Optimization process completed successfully")

        return FileResponse(
            xhtml_output,
            media_type="application/xhtml+xml",
            background=BackgroundTask(clean),
        )
    except Exception as e:
        logging.error(f"Error occurred during optimization: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during optimization process")"""

@app.get("/log/get")
async def log_get(
    # api_key: APIKey = Depends(get_api_key),
):
    try:
        return FileResponse("api.log")
    except Exception as e:
        logging.info(f"Erreur : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur : {e}")


@app.get("/log/delete")
async def log_delete(
    # api_key: APIKey = Depends(get_api_key),
):
    try:
        with open("api.log", "w") as f:
            f.write("")
        logging.info("Nouveau fichier log")
        return {"detail": "Fichier log supprimé avec succés"}
    except Exception as e:
        logging.info(f"Erreur : {e}")
        raise HTTPException(status_code=500, detail=f"Erreur : {e}")


@app.post("/optimise/remove/fontface")
async def remove_font_face(
    html_file: UploadFile = UploadFile(...),
    # api_key: APIKey = Depends(get_api_key),
):
    try:
        logging.info(f"Début de la supprsion de fontface du fichier html: {html_file.filename}")
        if not html_file.filename.endswith('html'): raise HTTPException(status_code=500, detail=f"Erreur : Veuillez choisir le fichier HTML")
        tmpdir = "tmp"
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)

        os.mkdir(tmpdir)
        file_path = Path(tmpdir) / html_file.filename
        with file_path.open("wb") as buffer:
            buffer.write(await html_file.read())
        html = RMF.remove_font_face(str(file_path))
        # Generate a html file
        path_file_html = f"{Path(tmpdir)}/{html_file.filename}"
        with open(path_file_html, "w", encoding="utf-8") as f:
            f.write(html)
        return FileResponse(path_file_html)

    except Exception as e:
        logging.error(
            f"Erreur lors de l'optimisation du fichier : {html_file.filename} - {e}"
        )
        raise HTTPException(status_code=500, detail=f"Erreur : {e}")


@app.post("/optimise/merge/fontface")
async def merge_font_face(
    html_file: UploadFile = UploadFile(...),
    xhtml_file: UploadFile = UploadFile(...),
    # api_key: APIKey = Depends(get_api_key),
):
    try:
        logging.info(f"Début de la fussion de fontface {xhtml_file.filename} et le fichier html tagé {html_file.filename}")
        if not html_file or not xhtml_file: raise HTTPException(status_code=500, detail=f"Erreur : Veuillez choisir les fichier HTML")
        tmpdir = "tmp"
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)

        os.mkdir(tmpdir)
        file_path_html = Path(tmpdir) / html_file.filename
        with file_path_html.open("wb") as file:
            file.write(await html_file.read())
        file_path_html_tag = Path(tmpdir) / xhtml_file.filename
        with open(file_path_html_tag, "wb") as file:
            file.write(await xhtml_file.read())
  
        full_html = RMF.fusion_file_tag_with_style(file_path_html, file_path_html_tag) 
        path_file_html = f"{Path(tmpdir)}/{html_file.filename}"
        with open(path_file_html, "w", encoding="utf-8") as f:
            f.write(full_html)
        return FileResponse(path_file_html)

    except Exception as e:
        logging.error(
            f"Erreur lors de l'optimisation du fichier : {html_file.filename} - {e}"
        )
        raise HTTPException(status_code=500, detail=f"Erreur : {e}")
    

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


@app.post("/optimise/merge/images")
async def merge_images(
        folder: UploadFile = UploadFile(...),
        # api_key: APIKey = Depends(get_api_key),
):
    #try:
    logging.info(f"Début de l'integration des images {folder.filename}")

    tmpdir = "tmp"
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)

    os.mkdir(tmpdir)

    folder_path = Path(tmpdir) / folder.filename
    with folder_path.open("wb") as buffer:
        buffer.write(await folder.read())

    extracted_folder = os.path.join(tmpdir, "extracted")
    os.makedirs(extracted_folder)

    with ZipFile(folder_path) as zip:
        zip.extractall(extracted_folder)


    xhtml_output = RMF.process_merge_images(
        extracted_folder + "/" + folder.filename.replace(".zip", "")
    )
    return FileResponse(
        xhtml_output,
        media_type="application/xhtml+xml",
        background=BackgroundTask(clean),
    )

        #except Exception as e:
        #    logging.error(
        #        f"Erreur lors de l'integration des images : {folder.filename} - {e}"
        #    )
        #    raise HTTPException(status_code=500, detail=f"Erreur : {e}")


@app.post("/convert_img_bs64/")
async def convert_img_bs64(zip_file: UploadFile = UploadFile(...)):
    if not zip_file.filename:
        raise HTTPException(status_code=400, detail="Please upload a zip file")
    elif not zip_file.filename.endswith(".zip"):
        raise HTTPException(status_code=400, detail="Please upload a zip file")
    try:
        tmpdir = "tmp"
        if os.path.exists(tmpdir): shutil.rmtree(tmpdir)
        os.mkdir(tmpdir)
        folder_path = Path(tmpdir) / zip_file.filename
        # copy zip file on dirctory tmp
        with open(folder_path, "wb") as file:
            shutil.copyfileobj(zip_file.file, file)
        # extract all content on tmp diroctory
        with zipfile.ZipFile(folder_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)
        # get new content file html and name of file html
        content, file_name = convert_html_img_bs64()
        if not content: raise HTTPException(status_code=400, detail="no content to create the new html file")
        # create a new file html with new content
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)

        return FileResponse(file_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/fix-thead")
async def fix_thead(file: UploadFile):
    # API endpoint to process an uploaded HTML or XHTML file and correct 
    # the issue of <thead> tags.
    
    # Args:
    # - file (UploadFile): The HTML or XHTML file to be processed.

    # Returns:
    # - FileResponse: The corrected file with <thead> tags replaced by <tbody> 
    #   when necessary.
      
    # Raises:
    # - HTTPException: If the file is not of the correct type or if an error occurs.
   
    # Check file extension
    if not file.filename.endswith(('.html', '.xhtml')):
        raise HTTPException(status_code=400, detail="Veuillez fournir un fichier HTML ou XHTML.")
   
    # Save temporary file
    with NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_file_path = tmp_file.name
 
    try:
        # Read HTML file 
        with open(tmp_file_path, "r", encoding="utf-8") as f:
            content = f.read()
 
        # Function to replace <thead> by <tbody>
        def replace_thead_without_tbody(match):
            table = match.group(0)  # Tag table content

            # Delete coms temporary
            table_cleaned = re.sub(r'<!--.*?-->', '', table, flags=re.DOTALL)
             
            # Check if <thead> is followed by <tbody>
            if not re.search(r'</thead>\s*<tbody>', table_cleaned, re.DOTALL):
                # Replace <thead> by <tbody> and </thead> by </tbody>
                table = re.sub(r'<thead([^>]*)>', r'<tbody\1>', table)
                table = re.sub(r'</thead>', r'</tbody>', table)
            return table
 
        # Apply regex to fix tables
        content_corrected = re.sub(r'<table[^>]*>.*?</table>', replace_thead_without_tbody, content, flags=re.DOTALL)
 
        # Save file
        corrected_file_path = tmp_file_path.replace(".html", "_corrected.html")
        with open(corrected_file_path, "w", encoding="utf-8") as corrected_file:
            corrected_file.write(content_corrected)
 
        # Return file
        return FileResponse(corrected_file_path, media_type='text/html', filename="corrected_file.html")
 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")
    
    
    