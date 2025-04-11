from bs4 import BeautifulSoup
import re, zipfile, os
import shutil, base64, os, subprocess, re, ftfy, multiprocessing
import tempfile, concurrent.futures, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import logging
from pathlib import Path

import os
import urllib.request
import zipfile
import shutil


def remove_font_face(html_file_path):
    # read content file html
    try:
        with open(html_file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except FileNotFoundError:
        logging.info(f"Error: File not found: {html_file_path}")

    # Charger le contenu HTML dans BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Trouver tous les éléments <style> contenant du CSS
    style_tags = soup.find_all('style')

    # Parcourir tous les éléments <style>
    for style_tag in style_tags:
        # Récupérer le contenu CSS
        css_content = style_tag.string

        font_faces = re.findall(r'@font-face\s*{[^}]*}', css_content)
    
        # Generate a str @font-face
        style = ""
        for font_face in font_faces:
            style += font_face
        
        # Si le contenu CSS contient un @font-face, le supprimer
        css_content = re.sub(r'@font-face\s*{[^}]*}', '', css_content)
        
        # Remplacer le contenu CSS dans l'élément <style>
        style_tag.string = css_content

    # Renvoyer le HTML modifié et le style
    return str(soup)

# part 2

def delete_folder_and_contents(path_directory):
    if os.path.isdir(path_directory):
        for root, dirs, files in os.walk(path_directory):
            for file in files:
                os.remove(os.path.join(root, file))
        for root, dirs, files in os.walk(path_directory, topdown=False):
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path_directory)

def get_style_on_html(content):
    # Trouver tous les éléments <style> contenant du CSS
    style_tags = content.find_all('style')
    # Parcourir tous les éléments <style>
    for style_tag in style_tags:
    # Récupérer le contenu CSS
        css_content = style_tag.string
        font_faces = re.findall(r'@font-face\s*{[^}]*}', css_content)
        # Generate a str @font-face
        style = ""
        for font_face in font_faces: style += font_face
        # Renvoyer le style
    return str(style)


def fusion_file_tag_with_style(input_file, input_file_html_tag):
    # get style on file html
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            html_content = file.read()
    except FileNotFoundError:
        logging.info(f"Error: File not found: {input_file}")
    soup = BeautifulSoup(html_content, 'html.parser')
    fontface = get_style_on_html(soup)
    # Retrieve the content of the html file.
    try:
        with open(input_file_html_tag, 'r', encoding='utf-8') as file:
            html_content_tag = file.read()
    except FileNotFoundError:
        logging.info(f"Error: File not found: {input_file_html_tag}")

    soup = BeautifulSoup(html_content_tag, "html.parser")
    body = soup.find("body")
    styles = soup.find_all("style")
    if not body or not styles: return "Error"
    body = str(body.prettify())
    style_fusion= ""
    for style in styles:
        style_fusion += style.text
    style_fusion += fontface
    html = f"""
                <html xmlns:iso4217='http://www.xbrl.org/2003/iso4217' xmlns:xbrli='http://www.xbrl.org/2003/instance' xmlns:xlink='http://www.w3.org/1999/xlink' xmlns:link='http://www.xbrl.org/2003/linkbase' xmlns:ix='http://www.xbrl.org/2013/inlineXBRL' xmlns:ixt='http://www.xbrl.org/inlineXBRL/transformation/2020-02-12' xmlns:xbrldi='http://xbrl.org/2006/xbrldi' xmlns='http://www.w3.org/1999/xhtml' xmlns:ifrs-full='https://xbrl.ifrs.org/taxonomy/2022-03-24/ifrs-full' xmlns:esef_cor='https://www.esma.europa.eu/taxonomy/2022-03-24/esef_cor' xmlns:natixis='http://www.natixis.com/taxonomy/2019-12-31/natixis_full_entry_point' xml:lang='fr'>
                <head>
                <meta http-equiv='Content-Type' content='text/html; charset = utf-8' />
                 <title>
                 </title>
                <style type='text/css'>
                {style_fusion}
                </style>
                </head>
                <body>
                {body}
                </body>
                </html>
                """
    return html


# REDUIRE LA TAILLE DES IMAGES
#%%
# SAVOIR SI LE HTML CONTIENT DES JPEG
def contain_jpeg(html):
    contain = False
    pattern = r"data:image/jpeg;base64,([^\'\"]+)"
    matches = re.findall(pattern, html)
    contain = len(matches) > 0
    return contain


# SUPPRIMER LES IMAGE JPEG
def supprimer_images(html):
    # Recherche de toutes les occurrences de l'image encodée en base64
    images_supprimees = re.findall(r"data:image/jpeg;base64,([^\'\"]+)", html)
    # Remplacement de chaque occurrence par une chaîne contenant le numéro de séquence correspondant
    for i, img in enumerate(images_supprimees, start=1):
        html = html.replace('data:image/jpeg;base64,' + img, 'data:image/jpeg;base64,' + str(i))    
    return html


# REDUIRE LA TAILLE DES IMAGES
def Reduce_image(data):
    png_data = base64.b64decode(data)
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_filename = temp_file.name
        temp_file.write(png_data)
    subprocess.run(["pngquant","--output", temp_filename, "--force", temp_filename])
    with open(temp_filename, "rb") as reduced_file:
        reduced_png_data = reduced_file.read()
    reduced_base64 = base64.b64encode(reduced_png_data).decode("utf-8")
    os.remove(temp_filename)
    return data, reduced_base64


# PARALELISER LA REDUCTION DES IMAGES POUR AUGMENTER LES PERFORMANCES
def Reduce_images(html):
    pattern = r"data:image/png;base64,([^\'\"]+)"
    matches = re.findall(pattern, html)

    pool = multiprocessing.Pool()
    results = pool.map(Reduce_image, matches)
    logging.info("La taille des images PNG a été reduite")
    pool.close()
    pool.join()
    for match, svg_base64 in results:
        html = html.replace(match, svg_base64)
    return html

def process_images(html_file, sup_image):
    html_file = Path(html_file)  # Ensure it's a Path object
    logging.info(f"🔍 Processing file: {html_file}")

    if not html_file.exists():
        logging.error(f"❌ File not found: {html_file}")
        return None

    try:
        with html_file.open("r", encoding="utf-8") as f:
            html = f.read()
            logging.info(f"✅ Successfully read HTML file: {html_file}")
    except Exception as e:
        logging.error(f"❌ Error reading HTML file: {e}")
        return None

    
    jpeg = contain_jpeg(html)
    logging.info(f"📸 Contains JPEG images? {jpeg}")

    try:
       
        logging.info("🔧 Reducing PNG images...")
        soup = Reduce_images(html)
        logging.info("✅ PNG image reduction complete")
    except Exception as e:
        logging.error(f"❌ Error reducing PNG images: {e}")
        return None

    if sup_image and jpeg:
        try:
            soup = supprimer_images(soup)
            print("✅ JPEG images successfully removed")
        except Exception as e:
            print(f"❌ Error removing JPEG images: {e}")
            return None
    else:
       print("ℹ️ JPEG removal not required or no JPEGs found")

   
    output_path = Path("tmp") / (html_file.stem + ".html")
    print(f"📁 Output path: {output_path}")

    try:
        with output_path.open("w", encoding="utf-8") as file:
            file.write(str(soup))
            print(f"✅ Processed file successfully written: {output_path}")
    except Exception as e:
        print(f"❌ Error writing processed file: {e}")
        return None

    if not output_path.exists():
        print(f"❌ Output file not found after writing: {output_path}")
        return None

    print(f"🎉 Image processing completed successfully: {output_path}")
    return output_path
#%%
#process_images("./URD_JC_DECAUX_2023_FR_202403291802.html",1)


#%%
# Remettre les JPEG
def remettre_images(html_modifie, html_original):
    print("1")
    # Recherche des images supprimées dans le HTML original et réinsertion
    images_supprimees = re.findall(r"data:image/jpeg;base64,([^\'\"]+)", html_original)
    print("2")
    for i, img in enumerate(images_supprimees, start=1):
        #html_modifie = html_modifie.replace('data:image/jpeg;base64,' + str(i), 'data:image/jpeg;base64,' + img)
        html_modifie = html_modifie.replace(f"data:image/jpeg;base64,{i}'", f"data:image/jpeg;base64,{img}'")
    print("3")
    return html_modifie

def process_merge_images(root):
    print("4")
    files = os.listdir(root)
    html_original_path = f'{root}/{[i for i in files if i.endswith(".html")][0]}'
    html_modifie_path = f'{root}/{[i for i in files if i.endswith(".xhtml")][0]}'
    print("5")
    with open(html_original_path, "r", encoding="utf-8") as file:
        html_original = file.read()
    print("6")
    with open(html_modifie_path, "r", encoding="utf-8") as file:
        html_modifie = file.read()
    print("7")
    # Remettre les images dans le HTML original
    html_avec_images = remettre_images(html_modifie, html_original)
    print("8")
    out_xhtml_file_path = root + '_with_img.xhtml'
    # Écrire le HTML avec les images réinsérées dans un nouveau fichier
    with open(out_xhtml_file_path, "w", encoding="utf-8") as file:
        file.write(html_avec_images)
    print("9")
    return out_xhtml_file_path

# %%
#process_merge_image(URD_JC_DECAUX_2023_FR_202403291802)