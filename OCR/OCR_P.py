import pytesseract
from PIL import Image
import pandas as pd
import os
import argparse
from datetime import datetime
import re

class ImageTextExtractor:
    def __init__(self, tesseract_path=None):
        """
        Initialize the ImageTextExtractor
        
        Args:
            tesseract_path (str): Path to tesseract executable (Windows only)
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
    
    def extract_text_from_image(self, image_path):
        """
        Extract text from a single image
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            str: Extracted text
        """
        try:
            # Open and preprocess image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Extract text using OCR
            text = pytesseract.image_to_string(image)
            
            return text.strip()
        
        except Exception as e:
            print(f"Error processing {image_path}: {str(e)}")
            return ""
    
    def extract_structured_data(self, text):
        """
        Extract structured data from text (customize based on your needs)
        
        Args:
            text (str): Raw extracted text
            
        Returns:
            dict: Structured data
        """
        # Example: Extract common patterns
        data = {
            'full_text': text,
            'lines': [line.strip() for line in text.split('\n') if line.strip()],
            'word_count': len(text.split()),
            'char_count': len(text),
            'numbers': re.findall(r'\d+(?:\.\d+)?', text),
            'emails': re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text),
            'phone_numbers': re.findall(r'\b\d{3}-\d{3}-\d{4}\b|\b\(\d{3}\)\s*\d{3}-\d{4}\b', text)
        }
        
        return data
    
    def process_single_image(self, image_path, output_format='text'):
        """
        Process a single image and return results
        
        Args:
            image_path (str): Path to image
            output_format (str): 'text' or 'excel'
            
        Returns:
            dict: Processing results
        """
        print(f"Processing: {image_path}")
        
        # Extract text
        raw_text = self.extract_text_from_image(image_path)
        
        if not raw_text:
            return None
        
        # Structure the data
        structured_data = self.extract_structured_data(raw_text)
        
        # Add metadata
        result = {
            'image_path': image_path,
            'image_name': os.path.basename(image_path),
            'processed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            **structured_data
        }
        
        return result
    
    def process_multiple_images(self, image_folder, output_format='text'):
        """
        Process multiple images from a folder
        
        Args:
            image_folder (str): Path to folder containing images
            output_format (str): 'text' or 'excel'
            
        Returns:
            list: List of processing results
        """
        supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif'}
        results = []
        
        for filename in os.listdir(image_folder):
            if any(filename.lower().endswith(ext) for ext in supported_formats):
                image_path = os.path.join(image_folder, filename)
                result = self.process_single_image(image_path, output_format)
                if result:
                    results.append(result)
        
        return results
    
    def output_to_text(self, results, output_file='extracted_text.txt'):
        """
        Output results to text file
        
        Args:
            results (list): Processing results
            output_file (str): Output file path
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("IMAGE TEXT EXTRACTION RESULTS\n")
            f.write("=" * 50 + "\n\n")
            
            for result in results:
                f.write(f"Image: {result['image_name']}\n")
                f.write(f"Processed: {result['processed_at']}\n")
                f.write(f"Word Count: {result['word_count']}\n")
                f.write(f"Character Count: {result['char_count']}\n")
                f.write("-" * 30 + "\n")
                f.write("EXTRACTED TEXT:\n")
                f.write(result['full_text'])
                f.write("\n\n" + "=" * 50 + "\n\n")
        
        print(f"Text output saved to: {output_file}")
    
    def output_to_excel(self, results, output_file='extracted_data.xlsx'):
        """
        Output results to Excel file
        
        Args:
            results (list): Processing results
            output_file (str): Output file path
        """
        # Prepare data for Excel
        excel_data = []
        
        for result in results:
            row = {
                'Image Name': result['image_name'],
                'Image Path': result['image_path'],
                'Processed At': result['processed_at'],
                'Word Count': result['word_count'],
                'Character Count': result['char_count'],
                'Full Text': result['full_text'],
                'Text Lines': '\n'.join(result['lines']),
                'Numbers Found': ', '.join(result['numbers']),
                'Emails Found': ', '.join(result['emails']),
                'Phone Numbers': ', '.join(result['phone_numbers'])
            }
            excel_data.append(row)
        
        # Create DataFrame and save to Excel
        df = pd.DataFrame(excel_data)
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Extracted Data', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Extracted Data']
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        print(f"Excel output saved to: {output_file}")

def main():
    """
    Main function with command-line interface
    """
    parser = argparse.ArgumentParser(description='Extract text from images and output to text or Excel')
    parser.add_argument('input', help='Input image file or folder path')
    parser.add_argument('-o', '--output', default='text', choices=['text', 'excel'], 
                       help='Output format (text or excel)')
    parser.add_argument('-f', '--file', help='Output file name')
    parser.add_argument('--tesseract-path', help='Path to tesseract executable (Windows)')
    
    args = parser.parse_args()
    
    # Initialize extractor
    extractor = ImageTextExtractor(tesseract_path=args.tesseract_path)
    
    # Process input
    if os.path.isfile(args.input):
        # Single image
        results = [extractor.process_single_image(args.input, args.output)]
        results = [r for r in results if r is not None]
    elif os.path.isdir(args.input):
        # Multiple images
        results = extractor.process_multiple_images(args.input, args.output)
    else:
        print("Error: Input path does not exist")
        return
    
    if not results:
        print("No text could be extracted from the images")
        return
    
    # Output results
    if args.output == 'text':
        output_file = args.file or 'extracted_text.txt'
        extractor.output_to_text(results, output_file)
    else:
        output_file = args.file or 'extracted_data.xlsx'
        extractor.output_to_excel(results, output_file)

if __name__ == "__main__":
    main()
