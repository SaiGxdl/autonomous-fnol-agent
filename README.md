# 🤖 Autonomous FNOL Processing Agent

A lightweight, deterministic system for processing **First Notice of Loss (FNOL)**
documents and routing insurance claims to the appropriate workflow.

This project is built as a **take-home / assessment solution**, with a strong focus on:

- ✅ Correctness  
- ✅ Explainability  
- ✅ Clean system design  
- ✅ Real-world insurance handling  

Enterprise-scale infrastructure and heavy dependencies are intentionally out of scope.

---

## 📌 Problem Statement

Insurance FNOL documents arrive in multiple formats (TXT, PDFs, scanned forms).
The goal of this agent is to:

- Extract key FNOL fields  
- Detect missing or inconsistent data  
- Classify the claim type  
- Route the claim using **deterministic, priority-based rules**  
- Provide a clear explanation for every routing decision  

All outputs are produced as **structured JSON**.

---

## 🧠 Approach (High-Level)

The system follows a simple, explainable pipeline:

```code
Input Document
↓
Text Extraction (TXT / PDF)
↓
Key-Value Field Extraction
↓
Schema Validation & Consistency Checks
↓
Priority-Based Routing Engine
↓
JSON Output + Reasoning

````

### Key Design Principles

- **No hallucination** — data is extracted only if explicitly present  
- **Key-Value aware parsing** — only `LABEL: VALUE` pairs are captured  
- **Graceful failure** — unreadable or blank documents are safely handled  
- **Deterministic routing** — no randomness, no hidden scoring  

---

## 📂 Supported Input Formats

| Format | Support | Notes |
|-----|------|-----|
| TXT | ✅ Full | Used to validate extraction logic |
| Text-based PDF | ✅ Partial | PDFs generated from Word / Docs |
| Scanned / template PDFs (ACORD) | ⚠️ Limited | Routed to Manual Review |

---

## ✨ Features

- Rule-based, schema-validated extraction
- Boilerplate & footer filtering (ACORD headers/footers ignored)
- Mandatory field detection
- Simple inconsistency checks
- Strict routing priority enforcement
- Clear, human-readable reasoning
- CLI-based execution for easy evaluation

---

## 🔀 Routing Rules (Strict Priority Order)

1. **Manual Review** *(Highest Priority)*  
   - Mandatory fields missing  
   - Document unreadable or contains no extractable text  

2. **Investigation**  
   - Claim description contains: `fraud`, `inconsistent`, `staged`  

3. **Specialist Queue**  
   - Claim type is `injury`  

4. **Fast-track**  
   - Estimated damage `< 25,000`  

If none apply → **Standard Processing**

---

## 🗂️ Project Structure

```text
autonomous-fnol-agent/
├── src/
│   ├── main.py            # CLI entry point
│   ├── loaders/           # File & folder loading
│   ├── extractors/        # TXT / PDF extraction
│   ├── validators/        # Schema & consistency checks
│   ├── routing/           # Routing rules
│   └── utils/             # Config & helpers
│
├── sample_docs/           # Example FNOL inputs
├── outputs/               # Generated JSON results
├── requirements.txt
├── .env.example
└── README.md
````

---

## 🚀 How to Run (Step-by-Step)

> These steps are intentionally detailed for easy evaluator execution.

### 1️⃣ Clone the Repository

```code
git clone https://github.com/SaiGxdl/autonomous-fnol-agent.git
cd autonomous-fnol-agent
```

---

### 2️⃣ Create a Virtual Environment

```code
python -m venv venv
```

Activate it:

* **macOS / Linux**

```code
source venv/bin/activate
```

* **Windows**

```code
venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```code
pip install -r requirements.txt
```

---

### 4️⃣ Run the Agent

To process all sample FNOL documents:

```code
python src/main.py --input sample_docs/
```

To process a single file:

```code
python src/main.py --input sample_docs/sample_fnol.txt
```

---

### 5️⃣ View Results

* Results are **printed to the console**
* JSON files are saved to the `outputs/` directory

---

## 📤 Example Outputs

### ❌ Blank / Template ACORD PDF

```json
{
  "recommendedRoute": "Manual Review",
  "reasoning": "Mandatory fields are missing from the document."
}
```

**Why?**
ACORD templates often contain labels without user-entered values.
The system correctly avoids guessing and routes such cases for manual handling.

---

### ✅ Valid FNOL (Low Damage)

```json
{
  "recommendedRoute": "Fast-track",
  "reasoning": "Estimated damage is below 25,000."
}
```

---

### 🚨 FNOL with Fraud Indicators

```json
{
  "recommendedRoute": "Investigation",
  "reasoning": "Fraud-related keywords detected in claim description."
}
```

---

## 🧠 Design Decisions & Assumptions

* Only explicit `LABEL: VALUE` pairs are extracted
* Boilerplate text is ignored
* Missing fields always override other routing rules
* No OCR or AI hallucination
* System behavior is deterministic and explainable

---

## 🔮 Future Enhancements

* OCR for scanned PDFs
* Expanded inconsistency detection
* REST API interface
* LLM-assisted extraction with validation
* Large-scale batch processing

---

## 👤 Author

**KKN Sai Charan**

[![GitHub](https://img.shields.io/badge/GitHub-SaiGxdl-181717?style=for-the-badge&logo=github)](https://github.com/SaiGxdl)
[![Email](https://img.shields.io/badge/Email-Contact-D14836?style=for-the-badge&logo=gmail)](mailto:saicharan.kkn@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-SAICHARAN-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/saicharankkn/)


---
