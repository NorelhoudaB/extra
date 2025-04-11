import os
import shutil
import logging
from fastapi import FastAPI, UploadFile, HTTPException, File,Response
from fastapi.responses import FileResponse, StreamingResponse
import io
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import REMOVE_MERGE_FONTFACE as RMF
from lxml import etree
import re

from bs4 import BeautifulSoup

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
        print(f"Starting image optimization: {file.filename}")
        file_path_html = Path(UPLOAD_DIR) / file.filename
        file_content = await file.read()

        if not file_content:
            print("The file is empty or corrupted")
            raise HTTPException(status_code=400, detail="Erreur : Le fichier est vide ou corrompu")

        print(f"Saving uploaded file: {file_path_html}")
        with file_path_html.open("wb") as f:
            f.write(file_content)

        output_file_path = RMF.process_images(file_path_html, del_jpeg)

        if not output_file_path or not output_file_path.exists():
            print("Processed file not found")
            raise HTTPException(status_code=500, detail="Erreur : Le fichier traité est introuvable")

        print(f"Optimized file saved: {output_file_path}")
        return FileResponse(output_file_path, filename=output_file_path.name, media_type="text/html")

    except Exception as e:
        print(f"Error optimizing file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur : {str(e)}")

@app.post("/fix-alt")
async def fix_alt(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    processed_file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    print(f"File saved: {file_path}")

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
    print(f"Updated file saved: {processed_file_path}")

    return FileResponse(processed_file_path, filename=file.filename, media_type="text/html")


@app.post("/convert-xhtml")
async def convert_xhtml(file: UploadFile = File(...)):
    print(f"Received XHTML file: {file.filename}")
    
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    base_name = os.path.splitext(file.filename)[0]
    xhtml_path = os.path.join(UPLOAD_DIR, file.filename)
    html_path = os.path.join(UPLOAD_DIR, f"{base_name}.html")

    with open(xhtml_path, "wb") as f:
        f.write(await file.read())
    print(f"Saved XHTML file: {xhtml_path}")

    def xhtml_to_html(xhtml_file, html_file):
        parser = etree.XMLParser(recover=True)
        tree = etree.parse(xhtml_file, parser)

        for elem in tree.xpath('//@*'):
            if elem is None:
                elem.getparent().remove(elem)

        html_content = etree.tostring(tree, method="html", encoding="unicode")

        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html_content)

    xhtml_to_html(xhtml_path, html_path)
    print(f"Converted HTML file saved: {html_path}")

   
    return FileResponse(html_path, filename=f"{base_name}.html", media_type="text/html")

# @app.post("/change-thead")
# async def change_thead(file: UploadFile):
#     print(f"Received file: {file.filename}")
#     if not file.filename.endswith(('.html', '.xhtml')):
#         print("Invalid file type")
#         raise HTTPException(400, "Invalid file type. Please upload an HTML or XHTML file.")

#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     processed_filename = file.filename.replace(".xhtml", ".xhtml").replace(".html", ".html")
#     processed_path = os.path.join(UPLOAD_DIR, processed_filename)

#     content = (await file.read()).decode('utf-8')

#     def replace_thead_if_no_tbody(table_content):
#         if re.search(r'<thead\b', table_content) and not re.search(r'<tbody\b', table_content):
#             return re.sub(r'</?thead\b', lambda x: x.group().replace('thead', 'tbody'), table_content)
#         return table_content

#     updated_content = re.sub(
#         r'<table[^>]*>.*?</table>',
#         lambda m: replace_thead_if_no_tbody(m.group()),
#         content,
#         flags=re.DOTALL
#     )

#     with open(processed_path, "w", encoding="utf-8") as f:
#         f.write(updated_content)

#     print(f"Processed file saved: {processed_path}")

#     return FileResponse(processed_path, filename=processed_filename, media_type="text/html")

@app.post("/fix-space")
async def fix_space(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    if not file.filename.endswith(('.html', '.xhtml')):
        print("Invalid file type")
        raise HTTPException(400, "Invalid file type. Please upload an HTML or XHTML file.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    processed_filename = file.filename.replace(".xhtml", ".xhtml").replace(".html", ".html")
    processed_path = os.path.join(UPLOAD_DIR, processed_filename)

    print(f"Saving uploaded file to {file_path}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    print("Replacing &#xa0; with spaces")
    content = content.replace("&#xa0;", " ")

    with open(processed_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Processed file saved to {processed_path}")

    return FileResponse(processed_path, filename=processed_filename, media_type="text/html")
 
@app.post("/fix-table")
async def fix_table_endpoint(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        html = contents.decode("utf-8")
    except Exception:
        raise HTTPException(status_code=400, detail="Erreur lors de la lecture du fichier.")
   
    updated_content = fix_table_html(html)
 
    corrected_file_path = os.path.join(UPLOAD_DIR, f"corrected_{file.filename}")
    with open(corrected_file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
 
    return FileResponse(corrected_file_path, filename=f"corrected_{file.filename}", media_type="text/html")

def fix_table_html(html: str) -> str:
    """
    Corrige la structure des balises <table> dans le HTML/XHTML :
      - Supprime les tables vides (contenant uniquement espaces et retours à la ligne).
      - Si la table ne contient pas de <tbody>, remplace <thead> et <tfoot> par <tbody>.
      - Si la table contient déjà un <tbody> (même avec <thead> et/ou <tfoot>), on ne modifie rien.
    """
    # 1. Supprimer les tables vides : <table ...> ne contenant que des espaces ou retours à la ligne
    html = re.sub(r'<table\b[^>]*>\s*</table>', '', html, flags=re.IGNORECASE)
 
    # 2. Pour chaque bloc <table>...</table> traité avec un callback
    def process_table(match):
        table_html = match.group(0)
        # Si la table contient déjà un <tbody>, on ne fait rien
        if re.search(r'<tbody\b', table_html, flags=re.IGNORECASE):
            return table_html
        # Sinon, on remplace les balises <thead> et <tfoot> par <tbody>
        # Remplacement pour les balises ouvrantes et fermantes
        table_html = re.sub(r'<(/?)(thead|tfoot)\b', r'<\1tbody', table_html, flags=re.IGNORECASE)
        return table_html
 
    # On parcourt chaque table complète en utilisant DOTALL pour inclure les retours à la ligne
    html = re.sub(r'(<table\b.*?</table>)', process_table, html, flags=re.IGNORECASE | re.DOTALL)
   
    return html


@app.post("/fix_id")
async def fix_id(file: UploadFile = File(...)):
    content = await file.read()
    html_content = content.decode("utf-8")
    
    pattern = r'(<div\b[^>]*?)\s+id\s*=\s*(["\'])\s*\2([^>]*?>)'
    html_content = re.sub(pattern, r'\1 \3', html_content, flags=re.IGNORECASE)
    html_content = re.sub(r'<div\s+>', '<div>', html_content)
    
    corrected_file = io.BytesIO(html_content.encode("utf-8"))
    return StreamingResponse(corrected_file, media_type="text/html", headers={
        "Content-Disposition": f'attachment; filename="corrected_{file.filename}"'
    })
import re
from bs4 import BeautifulSoup
from pathlib import Path
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil


def extract_content(file_paths):
    style_dict = {}
    body_dict = {}

    for file_path in file_paths:
        path = Path(file_path)
        filename = path.stem

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'lxml')
        
        style_content = '\n'.join(tag.string for tag in soup.find_all('style') if tag.string)
        body_content = soup.body.decode_contents() if soup.body else ''

        style_dict[filename] = style_content
        body_dict[filename] = body_content

    return style_dict, body_dict

def chk_cls(style_dict, input_files):
    tgt_cls = {'.A', '.batch', '.REPLACED', '.CHANGED'}

    def extract_cls(style_content):
        extracted_classes = {f'.{name}' for name in re.findall(r'\.([A-Za-z0-9_-]+)', style_content)}
        filtered_classes = {cls for cls in extracted_classes if any(cls.startswith(prefix) for prefix in tgt_cls)}
        return filtered_classes

    cls_sets = [extract_cls(style) for style in style_dict.values()]

    for i in range(len(cls_sets)):
        for j in range(i + 1, len(cls_sets)):
            if cls_sets[i] & cls_sets[j]:
                return i, j 
    return None

def rename_batch_classes_in_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        html = file.read()
    
    pattern = r'(?<=class=["\'])([^"\']+)(?=["\'])'
    def replace_classes(match):
        classes = match.group().split()
        replaced = [cls.replace('batch', 'REPLACED', 1) if cls.startswith('batch') else cls for cls in classes]
        return ' '.join(replaced)
    
    updated_html = re.sub(pattern, replace_classes, html)
    
    pattern = r'(?<=\.)(batch\w*)'
    updated_html = re.sub(pattern, lambda m: m.group().replace('batch', 'REPLACED', 1), updated_html)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(updated_html)

def rename_a_classes_in_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        html = file.read()
    
    pattern = r'(?<=class=["\'])([^"\']+)(?=["\'])'
    def replace_classes(match):
        classes = match.group().split()
        replaced = [cls.replace('A', 'CHANGED', 1) if cls.startswith('A') else cls for cls in classes]
        return ' '.join(replaced)
    
    updated_html = re.sub(pattern, replace_classes, html)
    
    pattern = r'(?<=\.)(A\w*)'
    updated_html = re.sub(pattern, lambda m: m.group().replace('A', 'CHANGED', 1), updated_html)
    
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(updated_html)

def combine_files(file_one, file_two, file_three):
    input_files = [file_one, file_two, file_three]
    style_dict, body_dict = extract_content(input_files)

    result = chk_cls(style_dict, input_files)

    if result is not None:
        i, j = result  
        rename_batch_classes_in_file(input_files[i], f"modified_batch_{i}.html")
        rename_a_classes_in_file(input_files[i], f"modified_A_{i}.html")
        
        updated_file = f"modified_batch_{i}.html"  
        input_files[i] = updated_file
        style_dict, body_dict = extract_content(input_files)  

    styles = '\n'.join([style_dict[Path(path).stem] for path in input_files])
    body_content = ''.join([body_dict[Path(path).stem] for path in input_files])

    path_two = Path(file_two)
    with open(path_two, 'r', encoding='utf-8') as f:
        content_two = f.read()

    soup_two = BeautifulSoup(content_two, 'lxml')

    if soup_two.head:
        style_tag = soup_two.head.find('style')
        if style_tag:
            style_tag.string = styles
        else:
            new_style_tag = soup_two.new_tag('style')
            new_style_tag.string = styles
            soup_two.head.append(new_style_tag)
    
    if soup_two.body:
        soup_two.body.clear()
        soup_two.body.append(BeautifulSoup(body_content, 'lxml'))

    output_file = path_two.parent / "merged_output.xhtml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup_two))


@app.post("/merge-files")
async def merge_files(file_one: UploadFile = File(...), file_two: UploadFile = File(...), file_three: UploadFile = File(...)):
    file_paths = []
    for file in [file_one, file_two, file_three]:
        temp_file_path = f"/tmp/{file.filename}"
        with open(temp_file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        file_paths.append(temp_file_path)
    
    merged_file = combine_files(file_paths[0], file_paths[1], file_paths[2])
    
    # Return the merged file as a response
    return FileResponse(merged_file, media_type="application/xhtml+xml", filename="merged_output.xhtml")
