import os
from img2table.ocr import TesseractOCR
from img2table.document import Image as Img2TableImage

def extract_table_from_image(image_path, excel_path):
    """
    Extract tabular data from an image and save to Excel.
    """
    if not os.path.exists(image_path):
        print(f"Image file '{image_path}' does not exist.")
        return

    # Initialize OCR engine
    ocr = TesseractOCR(lang="eng")
    
    # Load image
    doc = Img2TableImage(image_path)
    
    # Extract tables
    tables = doc.extract_tables(ocr=ocr)
    
    if not tables:
        print("No tables detected in the image.")
        return
    
    # Export the first detected table to Excel
    doc.to_xlsx(excel_path, ocr=ocr)
    print(f"Table(s) extracted and saved to: {excel_path}")

# Example usage
if __name__ == "__main__":
    input_image = "image.png"      # Replace with your image filename
    output_excel = "output_table.xlsx"  # Desired Excel output filename
    extract_table_from_image(input_image, output_excel)
