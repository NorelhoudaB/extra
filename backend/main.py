import os
import re
import io
import shutil
import logging
from pathlib import Path
from fastapi import FastAPI, UploadFile, HTTPException, File
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
from lxml import etree
import REMOVE_MERGE_FONTFACE as RMF

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("tmp")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/hello")
async def hello():
    return "Hello !!!"

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
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    img_pattern = re.compile(r'(<img\s+[^>]*?src="[^"]+")(?!\s+alt="image"\s)', re.IGNORECASE)
    def add_alt(match):
        return f'{match.group(1)} alt="image"'
    updated_content = img_pattern.sub(add_alt, html_content)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    return FileResponse(file_path, filename=file.filename, media_type="text/html")

@app.post("/convert-xhtml")
async def convert_xhtml(file: UploadFile = File(...)):
    base_name = os.path.splitext(file.filename)[0]
    xhtml_path = os.path.join(UPLOAD_DIR, file.filename)
    html_path = os.path.join(UPLOAD_DIR, f"{base_name}.html")
    with open(xhtml_path, "wb") as f:
        f.write(await file.read())
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(xhtml_path, parser)
    html_content = etree.tostring(tree, method="html", encoding="unicode")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return FileResponse(html_path, filename=f"{base_name}.html", media_type="text/html")

@app.post("/fix-space")
async def fix_space(file: UploadFile = File(...)):
    if not file.filename.endswith(('.html', '.xhtml')):
        raise HTTPException(400, "Invalid file type. Please upload an HTML or XHTML file.")
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("&#xa0;", " ")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return FileResponse(file_path, filename=file.filename, media_type="text/html")

@app.post("/fix-table")
async def fix_table_endpoint(file: UploadFile = File(...)):
    html = (await file.read()).decode("utf-8")
    updated_content = fix_table_html(html)
    corrected_file_path = os.path.join(UPLOAD_DIR, f"corrected_{file.filename}")
    with open(corrected_file_path, "w", encoding="utf-8") as f:
        f.write(updated_content)
    return FileResponse(corrected_file_path, filename=f"corrected_{file.filename}", media_type="text/html")

def fix_table_html(html: str) -> str:
    html = re.sub(r'<table\b[^>]*>\s*</table>', '', html, flags=re.IGNORECASE)
    def process_table(match):
        table_html = match.group(0)
        if re.search(r'<tbody\b', table_html, flags=re.IGNORECASE):
            return table_html
        return re.sub(r'<(/?)(thead|tfoot)\b', r'<\1tbody', table_html, flags=re.IGNORECASE)
    return re.sub(r'(<table\b.*?</table>)', process_table, html, flags=re.IGNORECASE | re.DOTALL)

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
    
    
#____________________________________________the merging files zone ____________________________________
 
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
def style_type(content: str) -> str:
    return content.replace('<style>', '<style type="text/css">')

def combine_files(file_one, file_two, file_three):
    input_files = [file_one, file_two, file_three]
    original_stems = [Path(p).stem for p in input_files]

    style_dict, body_dict = extract_content(input_files)
    result = chk_cls(style_dict, input_files)

    if result is not None:
        i, _ = result
        renamed_batch = UPLOAD_DIR / f"modified_batch_{i}.html"
        renamed_a = UPLOAD_DIR / f"modified_a_{i}.html"

        rename_batch_classes_in_file(input_files[i], renamed_batch)
        rename_a_classes_in_file(renamed_batch, renamed_a)

        input_files[i] = renamed_a
        style_dict, body_dict = extract_content(input_files)

    file_one_body = body_dict[Path(input_files[0]).stem]
    file_three_body = body_dict[Path(input_files[2]).stem]
    all_styles = '\n'.join([style_dict[Path(p).stem] for p in input_files if Path(p).stem in style_dict])

    with open(input_files[1], 'r', encoding='utf-8') as f:
        content_two = f.read()

    body_start = content_two.lower().find('<body')
    body_open_end = content_two.find('>', body_start)
    first_div_close = content_two.find('</div>', body_open_end)
    insert_after_div = first_div_close + len('</div>')
    insert_before_body_end = content_two.lower().rfind('</body>')

    new_content = (
        content_two[:insert_after_div] +
        file_one_body +
        content_two[insert_after_div:insert_before_body_end] +
        file_three_body +
        content_two[insert_before_body_end:]
    )

    head_end = new_content.lower().find('</head>')
    if head_end != -1:
        style_tag = f'<style>\n{all_styles}\n</style>\n'
        new_content = new_content[:head_end] + style_tag + new_content[head_end:]
        
    new_content = style_type(new_content)
    output_file = Path(input_files[1]).parent / "merged_output.xhtml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return str(output_file)


@app.post("/merge-files")
async def merge_files(file_one: UploadFile = File(...), file_two: UploadFile = File(...), file_three: UploadFile = File(...)):
    file_paths = []
    for file in [file_one, file_two, file_three]:
        temp_file_path = Path(UPLOAD_DIR) / file.filename
        with open(temp_file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        file_paths.append(temp_file_path)
    
    merged_file_path = combine_files(file_paths[0], file_paths[1], file_paths[2])
    
    # Clean up temp files
    for file_path in file_paths:
        try:
            os.unlink(file_path)
        except:
            pass
            
    return FileResponse(
        merged_file_path,   media_type="application/xhtml+xml",   filename="merged_output.xhtml"
    )