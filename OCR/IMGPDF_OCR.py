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
    thresh, img_bin = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    img_bin = 255 - img_bin

    kernel_len = np.array(img).shape[1] // 120
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    image_1 = cv2.erode(img_bin, vertical_kernel, iterations=3)
    vertical_lines = cv2.dilate(image_1, vertical_kernel, iterations=3)

    image_2 = cv2.erode(img_bin, horizontal_kernel, iterations=3)
    horizontal_lines = cv2.dilate(image_2, horizontal_kernel, iterations=3)

    img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
    img_vh = cv2.erode(~img_vh, kernel, iterations=2)
    thresh, img_vh = cv2.threshold(img_vh, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    (contours, bounding_boxes) = zip(*sorted(zip(contours, bounding_boxes), key=lambda b: b[1][1], reverse=False))

    boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if (w < 1000 and h < 500 and w > 30 and h > 30):  # Adjust filters as needed
            boxes.append([x, y, w, h])

    if not boxes:
        return None, pytesseract.image_to_string(gray)

    rows = []
    columns = []
    heights = [bounding_boxes[i][3] for i in range(len(bounding_boxes))]
    mean = np.mean(heights)

    previous = boxes[0]
    columns.append(boxes[0])
    for i in range(1, len(boxes)):
        if boxes[i][1] <= previous[1] + mean / 2:
            columns.append(boxes[i])
            previous = boxes[i]
            if i == len(boxes) - 1:
                rows.append(columns)
        else:
            rows.append(columns)
            columns = []
            previous = boxes[i]
            columns.append(boxes[i])

    total_cells = max(len(row) for row in rows)

    centers = [int(sorted([row[j][0] + row[j][2] / 2 for j in range(len(row))])) for row in rows]
    centers = np.unique(np.concatenate(centers))
    centers.sort()

    boxes_list = [[] for _ in range(len(rows))]
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            diff = abs(centers - (rows[i][j][0] + rows[i][j][2] / 4))
            min_diff = min(diff)
            index = np.argmin(diff)
            boxes_list[i].insert(index, rows[i][j])

    # Fill missing cells
    for i in range(len(boxes_list)):
        for j in range(total_cells):
            if len(boxes_list[i]) < total_cells:
                boxes_list[i].append([])

    # OCR on cells
    data = []
    full_text = ''
    for i in range(len(boxes_list)):
        row = []
        for j in range(len(boxes_list[i])):
            if len(boxes_list[i][j]) == 0:
                cell_text = ''
            else:
                x, y, w, h = boxes_list[i][j]
                cell_img = gray[y:y+h, x:x+w]
                cell_text = pytesseract.image_to_string(cell_img, config='--psm 6').strip()
            row.append(cell_text)
            full_text += cell_text + ' '
        data.append(row)
    full_text += '\n'

    df = pd.DataFrame(data)
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
            df.to_excel(writer, sheet_name=sheet_name, index=False)
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
                table_doc = doc.add_table(rows=df.shape[0] + 1, cols=df.shape[1])
                table_doc.style = 'Table Grid'
                for j, col in enumerate(df.columns):
                    table_doc.cell(0, j).text = str(col)
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