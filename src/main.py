import argparse
import json
from pathlib import Path

from loaders.document_loader import load_documents
from extractors.pdf_extractor import extract_text_from_pdf
from extractors.txt_extractor import extract_text_from_txt
from extractors.field_extractor import extract_fields
from validators.consistency import check_inconsistencies
from routing.rules import determine_route, find_missing_fields


def process_document(path: Path) -> dict:
    """
    Process a single FNOL document and return structured output.
    """

    # 1️⃣ Extract text safely
    try:
        if path.suffix.lower() == ".pdf":
            text = extract_text_from_pdf(path)
        else:
            text = extract_text_from_txt(path)
    except Exception as e:
        return {
            "status": "error",
            "file": path.name,
            "message": f"Extraction failed: {str(e)}",
        }

    # 2️⃣ Guard: unreadable / empty documents
    if not text or not text.strip():
        return {
            "status": "error",
            "file": path.name,
            "message": "Document could not be parsed or contains no extractable text",
            "recommendedRoute": "Manual Review",
            "reasoning": "Document is unreadable or has no extractable text. Manual intervention required.",
        }

    # 3️⃣ Field extraction & validation
    claim = extract_fields(text)
    missing_fields = find_missing_fields(claim)
    inconsistencies = check_inconsistencies(claim)

    # 4️⃣ Routing decision
    route, reasoning = determine_route(
        claim, missing_fields, inconsistencies
    )

    return {
        "status": "success",
        "file": path.name,
        "extractedFields": claim.model_dump(),
        "missingFields": missing_fields,
        "inconsistencies": inconsistencies,
        "recommendedRoute": route,
        "reasoning": reasoning,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Autonomous FNOL Processing Agent"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to FNOL file or folder",
    )
    args = parser.parse_args()

    documents = load_documents(args.input)

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    for doc in documents:
        result = process_document(doc)

        # Console output (reviewer-friendly)
        print(json.dumps(result, indent=2))

        # Persist output
        output_file = output_dir / f"{doc.stem}_output.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)


if __name__ == "__main__":
    main()
