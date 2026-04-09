from ocr import extract_text
from extractor import extract_invoice_data
from storage import save_to_excel
import os

INPUT_FILE = "../data/input/sample_invoice.pdf"
OUTPUT_FILE = "../data/output/invoices.xlsx"

def run_pipeline():
    print("Processing invoice...")

    text = extract_text(INPUT_FILE)

    if not text:
        print("No text extracted.")
        return

    data = extract_invoice_data(text)

    save_to_excel(data, OUTPUT_FILE)

    print("Extraction Complete ✅")
    print(data)

if __name__ == "__main__":
    run_pipeline()