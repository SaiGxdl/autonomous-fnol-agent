from pathlib import Path
from typing import List

SUPPORTED_EXTENSIONS = {".pdf", ".txt"}

def load_documents(input_path: str) -> List[Path]:
    """
    Accepts a file or directory path and returns a list of valid FNOL documents.
    """
    path = Path(input_path)

    if not path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")

    if path.is_file():
        if path.suffix.lower() in SUPPORTED_EXTENSIONS:
            return [path]
        else:
            raise ValueError("Unsupported file type. Only PDF and TXT allowed.")

    documents = []
    for file in path.iterdir():
        if file.suffix.lower() in SUPPORTED_EXTENSIONS:
            documents.append(file)

    if not documents:
        raise ValueError("No valid FNOL documents found.")

    return documents
