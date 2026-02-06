from pathlib import Path


def extract_text_from_txt(txt_path: Path) -> str:
    """
    Reads plain text FNOL file.
    Returns empty string if unreadable.
    """
    try:
        content = txt_path.read_text(encoding="utf-8", errors="ignore")
        return content.strip()
    except Exception as e:
        print(f"[WARN] TXT extraction failed for {txt_path.name}: {e}")
        return ""
