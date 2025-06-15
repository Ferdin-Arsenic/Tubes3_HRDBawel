import fitz  # PyMuPDF
import os

def pdf_to_string(pdf_path):
    doc = fitz.open(pdf_path)
    all_text = []
    for page in doc:
        text = page.get_text().replace("\n", " ").replace("\r", " ").lower()
        all_text.append(text)
    return " ".join(all_text)

def pdf_to_text(pdf_path, txt_output_path):
    doc = fitz.open(pdf_path)
    all_text = ""
    for page in doc:
        all_text += page.get_text().replace("\n", " ").replace("\r", " ").lower()
    with open(txt_output_path, "w", encoding="utf-8") as f:
        f.write(all_text)

def extract_all_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)  # Pastikan folder output ada

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            input_path = os.path.join(input_dir, filename)
            output_filename = os.path.splitext(filename)[0] + ".txt"
            output_path = os.path.join(output_dir, output_filename)

            pdf_to_text(input_path, output_path)


# Contoh penggunaan
# pdf_to_text("../../dataset/pdf/[INPUT].pdf", "../../dataset/pdf/[OUTPUT].pdf")
extract_all_pdfs("../../dataset/pdf/", "../../dataset/txt/")
