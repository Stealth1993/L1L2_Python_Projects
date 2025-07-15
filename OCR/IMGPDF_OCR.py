import os
from PIL import Image
import pytesseract
from img2table.document import Image as I2TImage, PDF as I2TPDF
from img2table.ocr import TesseractOCR
import pandas as pd
from pdf2image import convert_from_path
import PyPDF2
from docx import Document
from docx.shared import Inches
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

# Note: This script requires the following installations:
# pip install img2table pytesseract pandas openpyxl pdf2image PyPDF2 python-docx
# Additionally, you need to have Tesseract OCR installed on your system[](https://github.com/tesseract-ocr/tesseract)
# and Poppler for pdf2image[](https://pdf2image.readthedocs.io/en/latest/installation.html)

def get_pdf_page_count(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return len(reader.pages)

def populate_page_ranges(num_pages):
    ranges = ['All']
    if num_pages > 1:
        batch_size = 5 if num_pages <= 20 else 20 if num_pages <= 100 else 50
        for i in range(1, num_pages + 1, batch_size):
            end = min(i + batch_size - 1, num_pages)
            ranges.append(f"{i}-{end}")
    return ranges

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF or Image files", "*.pdf *.jpg *.jpeg *.png")])
    if file_path:
        entry_file_path.set(file_path)
        if file_path.lower().endswith('.pdf'):
            num_pages = get_pdf_page_count(file_path)
            page_ranges = populate_page_ranges(num_pages)
            combo_pages['values'] = page_ranges
            combo_pages.current(0)
        else:
            combo_pages['values'] = ['1']
            combo_pages.current(0)

def process_file():
    input_file = entry_file_path.get()
    if not input_file:
        messagebox.showerror("Error", "Please select a file.")
        return

    page_range = combo_pages.get()
    output_type = combo_output.get()

    if not page_range or not output_type:
        messagebox.showerror("Error", "Please select page range and output type.")
        return

    base_name = os.path.basename(input_file).rsplit('.', 1)[0]
    desktop = os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop")
    ocr = TesseractOCR(lang="eng", psm=6)
    text = ''
    tables = []

    if input_file.lower().endswith('.pdf'):
        num_pages = get_pdf_page_count(input_file)
        if page_range == 'All':
            start, end = 1, num_pages
        else:
            start, end = map(int, page_range.split('-'))
        pages_list = list(range(start, end + 1))

        doc = I2TPDF(input_file, pages=pages_list, detect_rotation=False)
        extracted = doc.extract_tables(ocr=ocr, implicit_rows=True, implicit_columns=True, borderless_tables=True, min_confidence=50)
        for page_tables in extracted.values():
            tables.extend(page_tables)

        # Convert selected pages to images for full text extraction
        page_imgs = convert_from_path(input_file, first_page=start, last_page=end)
        for page_img in page_imgs:
            text += pytesseract.image_to_string(page_img) + '\n\n'
    else:
        # Image
        doc = I2TImage(input_file)
        extracted_tables = doc.extract_tables(ocr=ocr, implicit_rows=True, implicit_columns=True, borderless_tables=True, min_confidence=50)
        tables.extend(extracted_tables)

        img = Image.open(input_file)
        text = pytesseract.image_to_string(img)

    # Now, based on selected output type
    ext_map = {'Excel': '.xlsx', 'TXT': '.txt', 'DOC': '.docx'}
    output_ext = ext_map[output_type]
    range_str = page_range.replace('-', '_') if page_range != 'All' else 'all'
    output = os.path.join(desktop, f"{base_name}_{range_str}{output_ext}")

    if output_type == 'Excel':
        writer = pd.ExcelWriter(output, engine='openpyxl')
        text_lines = pd.DataFrame({'Extracted Text': text.split('\n')})
        text_lines.to_excel(writer, sheet_name='Full Text', index=False)
        for i, table in enumerate(tables, 1):
            df = table.df
            df.to_excel(writer, sheet_name=f'Table {i}', index=False)
        writer.close()
    elif output_type == 'TXT':
        with open(output, 'w', encoding='utf-8') as f:
            f.write(text)
    elif output_type == 'DOC':
        doc = Document()
        doc.add_heading('Extracted Text', level=1)
        for line in text.splitlines():
            doc.add_paragraph(line)
        if tables:
            doc.add_heading('Extracted Tables', level=1)
            for i, table in enumerate(tables, 1):
                doc.add_heading(f'Table {i}', level=2)
                df = table.df
                table_doc = doc.add_table(rows=df.shape[0] + 1, cols=df.shape[1])
                table_doc.style = 'Table Grid'
                # Add header
                for j, col in enumerate(df.columns):
                    table_doc.cell(0, j).text = str(col)
                # Add rows
                for row_idx, row in df.iterrows():
                    for j, val in enumerate(row):
                        table_doc.cell(row_idx + 1, j).text = str(val)
        doc.save(output)

    messagebox.showinfo("Success", f"File saved to {output}")

def exit_app():
    root.quit()

# GUI
root = tk.Tk()
root.title("Data Extractor GUI")
root.geometry("500x300")

entry_file_path = tk.StringVar()

tk.Button(root, text="Select File", command=select_file).grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(root, text="Select Page Range:").grid(row=1, column=0, pady=10)
combo_pages = ttk.Combobox(root, values=[], state="readonly")
combo_pages.grid(row=1, column=1, padx=10)

tk.Label(root, text="Select Output Type:").grid(row=2, column=0, pady=10)
combo_output = ttk.Combobox(root, values=['Excel', 'TXT', 'DOC'], state="readonly")
combo_output.grid(row=2, column=1, padx=10)
combo_output.current(0)

tk.Button(root, text="Process", command=process_file).grid(row=3, column=0, pady=20, padx=20)
tk.Button(root, text="Exit", command=exit_app).grid(row=3, column=1, pady=20)

root.mainloop()