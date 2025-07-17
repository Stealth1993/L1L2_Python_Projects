import cv2
import pytesseract
import pandas as pd
import numpy as np
from PIL import Image
import os
import argparse
import sys
from datetime import datetime
import re
import json

class TableExtractor:
    def __init__(self, tesseract_path=None):
        """
        Initialize the TableExtractor
        
        Args:
            tesseract_path (str): Path to tesseract executable (Windows only)
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Configure tesseract for better table recognition
        self.ocr_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz ._-'
    
    def _enhance_image(self, gray_img):
        """Enhance image for better OCR results"""
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray_img, (1, 1), 0)
        
        # Apply adaptive threshold
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
        
        # Apply morphological operations to connect text
        kernel = np.ones((1, 1), np.uint8)
        enhanced = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        return enhanced
    
    def _detect_table_lines(self, image):
        """Detect horizontal and vertical lines in the table"""
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Apply threshold
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        
        # Detect horizontal lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        horizontal_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        
        # Detect vertical lines
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
        vertical_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        
        # Combine lines
        table_mask = cv2.addWeighted(horizontal_lines, 0.5, vertical_lines, 0.5, 0.0)
        
        return table_mask, horizontal_lines, vertical_lines
    
    def _extract_cells_opencv(self, image):
        """Extract table cells using OpenCV"""
        try:
            # Convert to grayscale
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            else:
                gray = image
            
            # Enhance image
            enhanced = self._enhance_image(gray)
            
            # Detect table lines
            table_mask, h_lines, v_lines = self._detect_table_lines(image)
            
            # Find contours
            contours, _ = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filter contours to find cells
            cells = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w > 30 and h > 15:  # Filter small noise
                    cells.append((x, y, w, h))
            
            # Sort cells by position (top to bottom, left to right)
            cells.sort(key=lambda cell: (cell[1], cell[0]))
            
            # Extract text from each cell
            cell_texts = []
            for x, y, w, h in cells:
                cell_img = enhanced[y:y+h, x:x+w]
                text = pytesseract.image_to_string(cell_img, config=self.ocr_config).strip()
                cell_texts.append({
                    'x': x, 'y': y, 'w': w, 'h': h,
                    'text': text
                })
            
            return cell_texts
            
        except Exception as e:
            print(f"Error in OpenCV cell extraction: {e}")
            return []
    
    def _group_cells_into_table(self, cells):
        """Group cells into rows and columns"""
        if not cells:
            return []
        
        # Sort cells by y-coordinate to group into rows
        cells.sort(key=lambda c: c['y'])
        
        # Group cells into rows based on y-coordinate proximity
        rows = []
        current_row = [cells[0]]
        
        for cell in cells[1:]:
            if abs(cell['y'] - current_row[0]['y']) < 20:  # Same row
                current_row.append(cell)
            else:  # New row
                rows.append(current_row)
                current_row = [cell]
        
        if current_row:
            rows.append(current_row)
        
        # Sort cells within each row by x-coordinate
        for row in rows:
            row.sort(key=lambda c: c['x'])
        
        # Convert to table format
        table_data = []
        for row in rows:
            row_data = [cell['text'] for cell in row]
            table_data.append(row_data)
        
        return table_data
    
    def _extract_using_ocr_parsing(self, image_path):
        """Extract table using OCR and intelligent parsing"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return None, "Could not load image"
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Enhance image
            enhanced = self._enhance_image(gray)
            
            # Extract all text with bounding boxes
            data = pytesseract.image_to_data(enhanced, output_type=pytesseract.Output.DICT)
            
            # Filter out empty text and organize by lines
            words = []
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 30:  # Confidence threshold
                    words.append({
                        'text': data['text'][i].strip(),
                        'left': data['left'][i],
                        'top': data['top'][i],
                        'width': data['width'][i],
                        'height': data['height'][i]
                    })
            
            # Group words into lines
            words.sort(key=lambda w: w['top'])
            lines = []
            current_line = []
            
            for word in words:
                if word['text']:
                    if not current_line or abs(word['top'] - current_line[0]['top']) < 10:
                        current_line.append(word)
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = [word]
            
            if current_line:
                lines.append(current_line)
            
            # Convert lines to table rows
            table_data = []
            for line in lines:
                line.sort(key=lambda w: w['left'])
                row_text = ' '.join([word['text'] for word in line])
                if row_text.strip():
                    # Try to split into columns based on spacing
                    columns = self._split_into_columns(row_text)
                    table_data.append(columns)
            
            return table_data, "Success"
            
        except Exception as e:
            return None, f"Error in OCR parsing: {e}"
    
    def _split_into_columns(self, text):
        """Split text into columns based on spacing patterns"""
        # Simple heuristic: split by multiple spaces
        columns = re.split(r'\s{2,}', text)
        return [col.strip() for col in columns if col.strip()]
    
    def method_1_img2table(self, image_path, output_path):
        """Method 1: Using img2table library"""
        try:
            from img2table.ocr import TesseractOCR
            from img2table.document import Image as Img2TableImage
            
            # Initialize OCR
            ocr = TesseractOCR(lang="eng")
            
            # Load the image
            doc = Img2TableImage(image_path)
            
            # Extract tables
            tables = doc.extract_tables(ocr=ocr)
            
            if tables:
                # Convert to DataFrame and save
                table_data = tables[0].df  # Get first table
                table_data.to_excel(output_path, index=False)
                return True, f"Successfully extracted table using img2table to {output_path}"
            else:
                return False, "No tables detected by img2table"
                
        except ImportError:
            return False, "img2table library not installed. Install with: pip install img2table"
        except Exception as e:
            return False, f"Error with img2table: {e}"
    
    def method_2_tablecv(self, image_path, output_path):
        """Method 2: Using tablecv library"""
        try:
            import tablecv
            
            # Extract table
            df = tablecv.extract_table(image_path=image_path)
            
            if df is not None and not df.empty:
                df.to_excel(output_path, index=False)
                return True, f"Successfully extracted table using tablecv to {output_path}"
            else:
                return False, "No table detected by tablecv"
                
        except ImportError:
            return False, "tablecv library not installed. Install with: pip install tablecv"
        except Exception as e:
            return False, f"Error with tablecv: {e}"
    
    def method_3_opencv(self, image_path, output_path):
        """Method 3: Using OpenCV for table detection"""
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return False, "Could not load image"
            
            # Extract cells
            cells = self._extract_cells_opencv(image)
            
            if not cells:
                return False, "No cells detected"
            
            # Group cells into table
            table_data = self._group_cells_into_table(cells)
            
            if table_data:
                # Convert to DataFrame
                df = pd.DataFrame(table_data)
                df.to_excel(output_path, index=False, header=False)
                return True, f"Successfully extracted table using OpenCV to {output_path}"
            else:
                return False, "Could not organize cells into table"
                
        except Exception as e:
            return False, f"Error with OpenCV method: {e}"
    
    def method_4_ocr_parsing(self, image_path, output_path):
        """Method 4: Using OCR with intelligent parsing"""
        try:
            table_data, message = self._extract_using_ocr_parsing(image_path)
            
            if table_data:
                # Convert to DataFrame
                df = pd.DataFrame(table_data)
                df.to_excel(output_path, index=False, header=False)
                return True, f"Successfully extracted table using OCR parsing to {output_path}"
            else:
                return False, message
                
        except Exception as e:
            return False, f"Error with OCR parsing: {e}"
    
    def extract_all_methods(self, image_path, output_dir="output"):
        """Try all extraction methods"""
        # Create output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        methods = [
            ("img2table", self.method_1_img2table),
            ("tablecv", self.method_2_tablecv),
            ("opencv", self.method_3_opencv),
            ("ocr_parsing", self.method_4_ocr_parsing)
        ]
        
        results = {}
        
        for method_name, method_func in methods:
            output_path = os.path.join(output_dir, f"{base_name}_{method_name}.xlsx")
            print(f"Trying {method_name}...")
            
            success, message = method_func(image_path, output_path)
            results[method_name] = {
                "success": success,
                "message": message,
                "output_path": output_path if success else None
            }
            
            print(f"  {message}")
        
        return results

def main():
    """Main function with command-line interface"""
    parser = argparse.ArgumentParser(description='Extract tabular data from images')
    parser.add_argument('image', help='Path to input image')
    parser.add_argument('-o', '--output', default='output', help='Output directory')
    parser.add_argument('-m', '--method', choices=['img2table', 'tablecv', 'opencv', 'ocr_parsing', 'all'], 
                       default='all', help='Extraction method to use')
    parser.add_argument('--tesseract-path', help='Path to tesseract executable (Windows)')
    
    args = parser.parse_args()
    
    # Check if image exists
    if not os.path.exists(args.image):
        print(f"Error: Image file '{args.image}' not found")
        sys.exit(1)
    
    # Initialize extractor
    extractor = TableExtractor(tesseract_path=args.tesseract_path)
    
    print(f"Processing image: {args.image}")
    print(f"Output directory: {args.output}")
    print("-" * 50)
    
    if args.method == 'all':
        results = extractor.extract_all_methods(args.image, args.output)
        
        # Print summary
        print("\n" + "="*50)
        print("EXTRACTION SUMMARY")
        print("="*50)
        successful_methods = []
        
        for method, result in results.items():
            status = "✓ SUCCESS" if result["success"] else "✗ FAILED"
            print(f"{method:15} {status}")
            if result["success"]:
                successful_methods.append(method)
        
        if successful_methods:
            print(f"\nSuccessful extractions: {len(successful_methods)}")
            print("Check the output directory for Excel files.")
        else:
            print("\nNo successful extractions. Please check your image quality or try different preprocessing.")
    
    else:
        # Use specific method
        base_name = os.path.splitext(os.path.basename(args.image))[0]
        output_path = os.path.join(args.output, f"{base_name}_{args.method}.xlsx")
        
        if not os.path.exists(args.output):
            os.makedirs(args.output)
        
        method_map = {
            'img2table': extractor.method_1_img2table,
            'tablecv': extractor.method_2_tablecv,
            'opencv': extractor.method_3_opencv,
            'ocr_parsing': extractor.method_4_ocr_parsing
        }
        
        success, message = method_map[args.method](args.image, output_path)
        
        if success:
            print(f"✓ SUCCESS: {message}")
        else:
            print(f"✗ FAILED: {message}")

if __name__ == "__main__":
    main()
