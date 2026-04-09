import streamlit as st
from src.ocr import extract_text
from src.extractor import extract_invoice_data
from src.storage import save_to_excel
import pandas as pd

st.title("📄 Invoice Automation Tool")

uploaded_file = st.file_uploader("Upload Invoice (PDF/JPG/PNG)")

if uploaded_file:
    # Save file with correct extension
    ext = uploaded_file.name.split(".")[-1]
    file_path = f"temp_file.{ext}"

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # OCR
    text = extract_text(file_path)

    #  Show OCR output
    st.subheader("Raw OCR Text")
    st.text(text[:1000])

    # Extract data
    data = extract_invoice_data(text)

    # Show JSON
    st.subheader("Extracted Data (JSON)")
    st.json(data)

    # Show Table (Dashboard feel)
    df = pd.DataFrame([data])
    st.subheader("📊 Invoice Table View")
    st.dataframe(df)

    # Save to Excel
    save_to_excel(data, "data/output/invoices.xlsx")

    st.success("Saved to Excel ✅")