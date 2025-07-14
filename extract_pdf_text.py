import os
from PyPDF2 import PdfReader # type: ignore
import logging

# Set up logging to track progress and errors
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define input and output directories
input_dir = "."  # Use current directory (sleepcorpus)
output_dir = "sleep_corpus_text"  # Where text files will be saved

# Create output directory if it doesn’t exist
os.makedirs(output_dir, exist_ok=True)

def extract_text_from_pdf(pdf_path, output_path):
    try:
        # Open and read the PDF
        reader = PdfReader(pdf_path)
        text = ""
        # Extract text from each page
        for page in reader.pages:
            page_text = page.extract_text() or ""  # Handle cases where text extraction fails
            text += page_text + "\n"
        
        # Save extracted text to a .txt file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        logging.info(f"Successfully extracted text from {pdf_path} to {output_path}")
    except Exception as e:
        logging.error(f"Failed to process {pdf_path}: {str(e)}")

def process_pdfs(input_dir, output_dir):
    # Debug: List all files found
    logging.info(f"Scanning directory: {input_dir}")
    pdf_count = 0
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(".pdf"):
                pdf_count += 1
                pdf_path = os.path.join(root, file)
                logging.info(f"Found PDF: {pdf_path}")
                # Create output filename (e.g., circadianrhythms.pdf -> circadianrhythms.txt)
                output_filename = os.path.splitext(file)[0] + ".txt"
                output_path = os.path.join(output_dir, output_filename)
                extract_text_from_pdf(pdf_path, output_path)
    
    if pdf_count == 0:
        logging.warning(f"No PDF files found in {input_dir}")

if __name__ == "__main__":
    logging.info("Starting PDF text extraction...")
    process_pdfs(input_dir, output_dir)
    logging.info("Text extraction complete!")