import os
import cv2
import numpy as np
import pytesseract
import pandas as pd
from pdf2image import convert_from_path
import PyPDF2
from docx import Document
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

# Note: This script requires the following installations:
# pip install opencv-python pytesseract pandas openpyxl pdf2image PyPDF2 python-docx
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

def extract_table_from_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 50, 150)

    # Detect lines using Probabilistic Hough Transform
    lines = cv2.HoughLinesP(canny, 1, np.pi/180, 50, minLineLength=100, maxLineGap=10)

    if lines is None:
        return None, pytesseract.image_to_string(gray)

    # Separate horizontal and vertical lines
    horizontal_lines = []
    vertical_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if abs(x1 - x2) < abs(y1 - y2):  # Vertical
            vertical_lines.append((min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))
        else:  # Horizontal
            horizontal_lines.append((min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)))

    # Filter overlapping lines
    def filter_overlapping_lines(lines, is_horizontal):
        if not lines:
            return []
        lines = sorted(lines, key=lambda l: l[1] if is_horizontal else l[0])
        filtered = [lines[0]]
        for current in lines[1:]:
            prev = filtered[-1]
            if is_horizontal:
                if abs(current[1] - prev[1]) > 5:
                    filtered.append(current)
            else:
                if abs(current[0] - prev[0]) > 5:
                    filtered.append(current)
        return filtered

    horizontal_lines = filter_overlapping_lines(horizontal_lines, True)
    vertical_lines = filter_overlapping_lines(vertical_lines, False)

    if len(horizontal_lines) < 2 or len(vertical_lines) < 2:
        return None, pytesseract.image_to_string(gray)

    # Extract cells
    table_data = []
    full_text = ''
    for i in range(len(horizontal_lines) - 1):
        row = []
        y1 = horizontal_lines[i][1]
        y2 = horizontal_lines[i+1][1]
        for j in range(len(vertical_lines) - 1):
            x1 = vertical_lines[j][0]
            x2 = vertical_lines[j+1][0]
            cell = gray[y1:y2, x1:x2]
            text = pytesseract.image_to_string(cell, config='--psm 6').strip()
            row.append(text)
            full_text += text + '\t'
        table_data.append(row)
        full_text += '\n'

    df = pd.DataFrame(table_data)
    return df, full_text.strip()

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
    all_dfs = []
    all_text = ''

    if input_file.lower().endswith('.pdf'):
        num_pages = get_pdf_page_count(input_file)
        if page_range == 'All':
            start, end = 1, num_pages
        else:
            start, end = map(int, page_range.split('-'))
        page_imgs = convert_from_path(input_file, first_page=start, last_page=end)
        for idx, page_img in enumerate(page_imgs, start=start):
            temp_path = os.path.join(desktop, f"temp_page_{idx}.jpg")
            page_img.save(temp_path, 'JPEG')
            df, text = extract_table_from_image(temp_path)
            if df is not None:
                all_dfs.append((f"Page {idx}", df))
            all_text += text + '\n\n'
            os.remove(temp_path)
    else:
        df, text = extract_table_from_image(input_file)
        if df is not None:
            all_dfs.append(("Table 1", df))
        all_text = text

    has_tables = len(all_dfs) > 0

    ext_map = {'Excel': '.xlsx', 'TXT': '.txt', 'DOC': '.docx'}
    output_ext = ext_map[output_type]
    range_str = page_range.replace('-', '_') if page_range != 'All' else 'all'
    output = os.path.join(desktop, f"{base_name}_{range_str}{output_ext}")

    if output_type == 'Excel':
        writer = pd.ExcelWriter(output, engine='openpyxl')
        text_df = pd.DataFrame({'Extracted Text': all_text.split('\n')})
        text_df.to_excel(writer, sheet_name='Full Text', index=False)
        for sheet_name, df in all_dfs:
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
        writer.close()
    elif output_type == 'TXT':
        with open(output, 'w', encoding='utf-8') as f:
            f.write(all_text)
    elif output_type == 'DOC':
        doc = Document()
        doc.add_heading('Extracted Text', level=1)
        doc.add_paragraph(all_text)
        if has_tables:
            doc.add_heading('Extracted Tables', level=1)
            for sheet_name, df in all_dfs:
                doc.add_heading(sheet_name, level=2)
                table_doc = doc.add_table(rows=df.shape[0], cols=df.shape[1])
                table_doc.style = 'Table Grid'
                for row_idx, row in df.iterrows():
                    for j, val in enumerate(row):
                        table_doc.cell(row_idx, j).text = str(val) if pd.notnull(val) else ''
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