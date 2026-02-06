import pdfplumber
from pathlib import Path


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Attempts to extract text from a PDF.
    Returns empty string if PDF has no extractable text.
    """
    text_chunks = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_chunks.append(page_text)
    except Exception as e:
        print(f"[WARN] PDF extraction failed for {pdf_path.name}: {e}")
        return ""

    return "\n".join(text_chunks).strip()
