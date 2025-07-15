import os
from PIL import Image
import pytesseract
import pandas as pd
from pdf2image import convert_from_path
import PyPDF2
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import torch
from transformers import DetrImageProcessor, TableTransformerForObjectDetection
import numpy as np
import cv2
from docx import Document

# Note: Ensure Tesseract OCR is installed and added to PATH

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
    image = Image.open(image_path).convert("RGB")
    # Preprocess the image for better OCR and detection
    image_np = np.array(image)
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    image = Image.fromarray(thresh).convert("RGB")
    text = pytesseract.image_to_string(image)

    # Table Detection
    detection_processor = DetrImageProcessor()
    detection_model = TableTransformerForObjectDetection.from_pretrained(
        "microsoft/table-transformer-detection"
    )

    inputs = detection_processor(images=image, return_tensors="pt")
    outputs = detection_model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]])
    detection_results = detection_processor.post_process_object_detection(outputs, threshold=0.7, target_sizes=target_sizes)[0]

    tables = []
    label_dict = detection_model.config.id2label
    for score, label, box in zip(detection_results["scores"], detection_results["labels"], detection_results["boxes"]):
        if label_dict[label.item()] == 'table' and score > 0.7:
            crop_box = (box[0].item(), box[1].item(), box[2].item(), box[3].item())
            cropped_table = image.crop(crop_box)

            # Table Structure Recognition
            structure_processor = DetrImageProcessor()
            structure_model = TableTransformerForObjectDetection.from_pretrained(
                "microsoft/table-transformer-structure-recognition"
            )

            structure_inputs = structure_processor(images=cropped_table, return_tensors="pt")
            structure_outputs = structure_model(**structure_inputs)
            structure_target_sizes = torch.tensor([cropped_table.size[::-1]])
            structure_results = structure_processor.post_process_object_detection(structure_outputs, threshold=0.5, target_sizes=structure_target_sizes)[0]

            structure_label_dict = structure_model.config.id2label

            # Get columns
            columns = [box.tolist() for idx, lbl in enumerate(structure_results['labels']) if structure_label_dict[lbl.item()] == 'table column']
            columns.sort(key=lambda x: x[0])  # sort by xmin

            # Get rows including header
            rows = [box.tolist() for idx, lbl in enumerate(structure_results['labels']) if structure_label_dict[lbl.item()] in ['table row', 'table column header']]
            rows.sort(key=lambda x: x[1])  # sort by ymin

            if not rows or not columns:
                continue

            has_header = any(structure_label_dict[lbl.item()] == 'table column header' for lbl in structure_results['labels'])

            if has_header:
                header_row = rows[0]
                data_rows = rows[1:]
            else:
                header_row = None
                data_rows = rows

            # Extract column names
            column_names = []
            for i in range(len(columns)):
                cell_xmin = columns[i][0]
                cell_xmax = columns[i][2]
                cell_ymin = header_row[1] if header_row else 0
                cell_ymax = header_row[3] if header_row else cropped_table.size[1]
                cell_img = cropped_table.crop((cell_xmin, cell_ymin, cell_xmax, cell_ymax))
                cell_np = np.array(cell_img)
                if len(cell_np.shape) == 2:
                    cell_np = cv2.cvtColor(cell_np, cv2.COLOR_GRAY2RGB)
                cell_gray = cv2.cvtColor(cell_np, cv2.COLOR_RGB2GRAY)
                cell_thresh = cv2.adaptiveThreshold(cell_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                cell_pil = Image.fromarray(cell_thresh)
                # Resize if small
                if cell_pil.width < 100 or cell_pil.height < 20:
                    cell_pil = cell_pil.resize((cell_pil.width * 3, cell_pil.height * 3))
                cell_text = pytesseract.image_to_string(cell_pil, config='--psm 7').strip()
                column_names.append(cell_text if cell_text else f"Column {i+1}")

            # Extract data rows
            data = []
            for row in data_rows:
                row_data = []
                for i in range(len(columns)):
                    cell_xmin = columns[i][0]
                    cell_xmax = columns[i][2]
                    cell_ymin = row[1]
                    cell_ymax = row[3]
                    cell_img = cropped_table.crop((cell_xmin, cell_ymin, cell_xmax, cell_ymax))
                    cell_np = np.array(cell_img)
                    if len(cell_np.shape) == 2:
                        cell_np = cv2.cvtColor(cell_np, cv2.COLOR_GRAY2RGB)
                    cell_gray = cv2.cvtColor(cell_np, cv2.COLOR_RGB2GRAY)
                    cell_thresh = cv2.adaptiveThreshold(cell_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                    cell_pil = Image.fromarray(cell_thresh)
                    # Resize if small
                    if cell_pil.width < 100 or cell_pil.height < 20:
                        cell_pil = cell_pil.resize((cell_pil.width * 3, cell_pil.height * 3))
                    cell_text = pytesseract.image_to_string(cell_pil, config='--psm 7').strip()
                    row_data.append(cell_text)
                data.append(row_data)

            df = pd.DataFrame(data, columns=column_names)
            tables.append(df)

    return tables, text

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
    all_tables = []
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
            tables, text = extract_table_from_image(temp_path)
            all_tables.extend([(f"Page {idx} Table {j+1}", df) for j, df in enumerate(tables)])
            all_text += text + '\n\n'
            os.remove(temp_path)
    else:
        tables, text = extract_table_from_image(input_file)
        all_tables.extend([(f"Table {j+1}", df) for j, df in enumerate(tables)])
        all_text = text

    has_tables = len(all_tables) > 0

    ext_map = {'Excel': '.xlsx', 'TXT': '.txt', 'DOC': '.docx'}
    output_ext = ext_map[output_type]
    range_str = page_range.replace('-', '_') if page_range != 'All' else 'all'
    output = os.path.join(desktop, f"{base_name}_{range_str}{output_ext}")

    if output_type == 'Excel':
        writer = pd.ExcelWriter(output, engine='openpyxl')
        text_df = pd.DataFrame({'Extracted Text': all_text.split('\n')})
        text_df.to_excel(writer, sheet_name='Full Text', index=False)
        for sheet_name, df in all_tables:
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # Sheet name limit 31 chars
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
            for sheet_name, df in all_tables:
                doc.add_heading(sheet_name, level=2)
                table_doc = doc.add_table(rows=df.shape[0] + 1, cols=df.shape[1])
                table_doc.style = 'Table Grid'
                for j, col in enumerate(df.columns):
                    table_doc.cell(0, j).text = str(col)
                for row_idx, row in df.iterrows():
                    for j, val in enumerate(row):
                        table_doc.cell(row_idx + 1, j).text = str(val) if pd.notnull(val) else ''
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