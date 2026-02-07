import os
import fitz  # PyMuPDF


def load_text_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf_file(file_path: str) -> str:
    """
    Extract text from PDF using PyMuPDF.
    """
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        page_text = page.get_text("text")
        if page_text:
            text += page_text + "\n"

    doc.close()
    return text


def load_documents(data_dir: str):
    """
    Load TXT, MD, and PDF documents from a directory.
    """
    documents = []

    for file_name in os.listdir(data_dir):
        file_path = os.path.join(data_dir, file_name)
        text = ""

        if file_name.endswith((".txt", ".md")):
            text = load_text_file(file_path)

        elif file_name.endswith(".pdf"):
            text = load_pdf_file(file_path)

        else:
            continue

        if not text.strip():
            print(f"Skipping empty document: {file_name}")
            continue

        documents.append({
            "text": text,
            "metadata": {
                "source": file_name,
                "policy_type": file_name.split(".")[0].lower()
            }
        })

    return documents
