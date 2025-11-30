import os
import fitz  # PyMuPDF
from pypdf import PdfReader, PdfWriter

def merge_pdfs(file_list, output_path):
    """Merges multiple PDF files into one."""
    merger = PdfWriter()
    for pdf in file_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

def split_pdf(file_path, output_dir, range_str=None):
    """
    Splits a PDF file.
    If range_str is provided (e.g., "1-3,5"), extracts those pages.
    Otherwise, extracts all pages as separate files.
    """
    reader = PdfReader(file_path)
    
    if range_str:
        # Parse range string
        # This is a simplified parser; for production, more robust parsing is needed
        pages_to_extract = set()
        parts = range_str.split(',')
        for part in parts:
            if '-' in part:
                start, end = map(int, part.split('-'))
                pages_to_extract.update(range(start - 1, end)) # 0-indexed
            else:
                pages_to_extract.add(int(part) - 1) # 0-indexed
        
        writer = PdfWriter()
        for page_num in sorted(pages_to_extract):
            if 0 <= page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])
        
        output_filename = os.path.join(output_dir, f"split_{os.path.basename(file_path)}")
        writer.write(output_filename)
        writer.close()
        
    else:
        # Extract all pages
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            output_filename = os.path.join(output_dir, f"{base_name}_page_{i+1}.pdf")
            writer.write(output_filename)
            writer.close()

def images_to_pdf(image_list, output_path):
    """Converts a list of images to a single PDF using PyMuPDF."""
    doc = fitz.open()
    for img_path in image_list:
        img = fitz.open(img_path)
        rect = img[0].rect
        pdfbytes = img.convert_to_pdf()
        img.close()
        imgPDF = fitz.open("pdf", pdfbytes)
        page = doc.new_page(width=rect.width, height=rect.height)
        page.show_pdf_page(rect, imgPDF, 0)
    doc.save(output_path)
    doc.close()

def pdf_to_images(pdf_path, output_dir):
    """Converts each page of a PDF to an image."""
    doc = fitz.open(pdf_path)
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    for i, page in enumerate(doc):
        pix = page.get_pixmap()
        output_filename = os.path.join(output_dir, f"{base_name}_page_{i+1}.png")
        pix.save(output_filename)

def compress_pdf(file_path, output_path):
    """Compresses a PDF file using PyMuPDF."""
    doc = fitz.open(file_path)
    # garbage=4: aggressive garbage collection (deduplication)
    # deflate=True: compress uncompressed streams
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()
