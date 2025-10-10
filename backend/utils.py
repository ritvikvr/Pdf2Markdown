from pdfminer.high_level import extract_text
import tabula
import fitz  # PyMuPDF
import pandas as pd
import pytesseract
from PIL import Image
import os
import re

def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def extract_tables_from_pdf(pdf_path):
    try:
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    except Exception:
        tables = []
    md_tables = []
    for table in tables:
        md_tables.append(table.to_markdown(index=False))
    return "\n\n".join(md_tables)

def extract_images_from_pdf(pdf_path, out_dir='images/'):
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    img_markdown = []
    saved_images = []
    for i, page in enumerate(doc):
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:
                img_filename = f"image_{i}_{img_index}.png"
                img_path = os.path.join(out_dir, img_filename)
                pix.save(img_path)
                img_markdown.append(f"![Image]({img_path})")
                saved_images.append(img_path)
            pix = None
    return "\n".join(img_markdown), saved_images

def ocr_images(image_paths):
    ocr_texts = []
    for img_path in image_paths:
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
        ocr_texts.append(f"### OCR Extracted Text from {img_path}\n{text}\n")
    return "\n".join(ocr_texts)

def enhanced_markdown_postprocessing(text_raw):
    lines = text_raw.splitlines()
    md_lines = []
    for line in lines:
        line = line.strip()
        if line.isupper() and len(line) > 3:
            md_lines.append(f"## {line}")
        elif line.startswith(("-", "*", "•")):
            md_lines.append(f"- {line[1:].strip()}")
        elif re.match(r'^\d+\.\s', line):
            md_lines.append(f"1. {line.split('.',1)[1].strip()}")
        else:
            md_lines.append(line)
    filtered_md = [l for l in md_lines if l.strip() != ""]
    return "\n".join(filtered_md)

def pdf_to_markdown(pdf_path):
    text_md = extract_text_from_pdf(pdf_path)
    text_md = enhanced_markdown_postprocessing(text_md)
    tables_md = extract_tables_from_pdf(pdf_path)
    images_md, saved_image_paths = extract_images_from_pdf(pdf_path)
    ocr_text = ""
    if saved_image_paths:
        ocr_text = ocr_images(saved_image_paths)
    md_content = "# PDF Converted to Markdown\n\n"
    if text_md:
        md_content += "## Text\n" + text_md + "\n\n"
    if tables_md:
        md_content += "## Tables\n" + tables_md + "\n\n"
    if images_md:
        md_content += "## Images\n" + images_md + "\n\n"
    if ocr_text:
        md_content += "## OCR Results\n" + ocr_text + "\n\n"
    return md_content
