🤖 Autonomous FNOL Processing Agent

This project implements a lightweight autonomous agent that processes
First Notice of Loss (FNOL) documents and routes insurance claims to the
appropriate workflow.

The solution is designed as a take-home / assessment project, with emphasis on
clarity, correctness, explainability, and clean system design, rather than
enterprise-scale infrastructure.

📌 Problem Overview

The agent performs the following tasks:

Extracts key fields from FNOL documents (TXT and PDF)

Identifies missing or inconsistent information

Classifies and routes claims using deterministic rules

Provides a short, explainable reason for each routing decision

Outputs results in a structured JSON format

📂 Supported Input Formats

TXT — fully supported and used to validate extraction logic

Text-based PDF — supported (e.g., PDFs generated from Word/Docs)

Scanned / template PDFs (e.g., ACORD forms)

Detected automatically

Safely routed to Manual Review if no extractable data is present

⚠️ OCR is intentionally excluded from this assessment scope and listed as a future enhancement.

✨ Features

Hybrid extraction approach (rule-based, schema-validated)

Key-value aware parsing (LABEL: VALUE)

Boilerplate and footer text filtering (e.g., ACORD headers/footers)

Mandatory field detection

Priority-based routing engine

Deterministic, explainable outputs

Graceful handling of unreadable or blank documents

🔀 Supported Routing Rules

Routing is applied in strict priority order:

Manual Review (Highest Priority)

Triggered if mandatory fields are missing

Triggered if the document cannot be parsed or has no extractable text

Investigation

Triggered if the claim description contains keywords such as
fraud, inconsistent, or staged

Specialist Queue

Triggered if the claim type is injury

Fast-track

Triggered if estimated damage is below 25,000

If none of the above conditions apply, the claim is routed to
Standard Processing.

🗂️ Project Structure
autonomous-fnol-agent/
├── src/
│   ├── main.py            # CLI entry point
│   ├── loaders/          # File and folder loading
│   ├── extractors/       # TXT/PDF extraction logic
│   ├── validators/       # Schema & consistency checks
│   ├── routing/          # Deterministic routing rules
│   └── utils/            # Configuration & helpers
│
├── sample_docs/
│   ├── ACORD-Automobile-Loss-Notice-12.05.16.pdf
│   ├── review_docs.pdf
│   └── sample_fnol.txt
│
├── outputs/              # Generated JSON results
├── requirements.txt
├── .env.example
└── README.md

🚀 How to Run
1️⃣ Environment Setup
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt

2️⃣ Run the Agent
python src/main.py --input sample_docs/


Results are printed to the console

JSON outputs are saved in the outputs/ directory

📤 Example Outputs
❌ Blank or Template ACORD PDF
{
  "recommendedRoute": "Manual Review",
  "reasoning": "Mandatory fields are missing from the document."
}


Explanation:
ACORD FNOL templates often contain labels without user-entered values.
The system distinguishes between form labels, boilerplate text, and actual inputs,
and safely routes such cases to manual review.

✅ Valid FNOL Document (Low Damage)
{
  "recommendedRoute": "Fast-track",
  "reasoning": "Estimated damage is below 25,000."
}

🚨 FNOL with Fraud Indicators
{
  "recommendedRoute": "Investigation",
  "reasoning": "Fraud-related keywords detected in claim description."
}

🧠 Design Decisions & Assumptions

Extraction only captures values that appear explicitly as LABEL: VALUE

Boilerplate text (e.g., ACORD headers, footers, page numbers) is ignored

No data is inferred or hallucinated

Missing mandatory fields always override other routing rules

OCR support is intentionally excluded and listed as a future enhancement

🔮 Future Enhancements

OCR support for scanned PDFs

Expanded inconsistency detection

REST API interface

LLM-assisted extraction with validation

Batch processing optimizations

📝 Notes

This project is intentionally lightweight and deterministic to match assessment
expectations and to ensure all routing decisions are fully explainable.