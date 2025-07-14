import os
from nltk.tokenize import sent_tokenize # type: ignore
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Input and output directories
input_dir = "sleep_corpus_text"  # Where your .txt files are
output_dir = "text_chunks"  # Where chunked files will be saved

# Create output directory if it doesn’t exist
os.makedirs(output_dir, exist_ok=True)

def chunk_text(text, max_tokens=500):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk.split()) + len(sentence.split()) <= max_tokens:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def process_texts(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_dir, filename)
            logging.info(f"Processing {input_path}")
            with open(input_path, "r", encoding="utf-8") as f:
                text = f.read()
            
            chunks = chunk_text(text)
            base_name = os.path.splitext(filename)[0]
            for i, chunk in enumerate(chunks):
                output_filename = f"{base_name}_chunk_{i}.txt"
                output_path = os.path.join(output_dir, output_filename)
                with open(output_path, "w", encoding="utf-8") as f_out:
                    f_out.write(chunk)
                logging.info(f"Created chunk: {output_path}")

if __name__ == "__main__":
    logging.info("Starting text chunking...")
    process_texts(input_dir, output_dir)
    logging.info("Text chunking complete!")