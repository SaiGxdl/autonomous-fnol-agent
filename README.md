# Autonomous FNOL Processing Agent

This project implements a lightweight autonomous agent that processes
First Notice of Loss (FNOL) documents and routes insurance claims to the
appropriate workflow.

The solution is designed as an assessment project, focusing on clarity,
correctness, explainability, and clean system design rather than
enterprise-scale infrastructure.

---

## Features

- Supports FNOL documents in TXT and text-based PDF formats
- Extracts key insurance claim fields
- Detects missing and inconsistent information
- Routes claims using deterministic, priority-based rules
- Produces structured JSON output with clear reasoning
- Gracefully handles unreadable or scanned PDFs

---

## Supported Routing Rules

Routing is applied in strict priority order:

1. **Investigation Flag**
   - Triggered if the claim description contains keywords such as
     `fraud`, `inconsistent`, or `staged`

2. **Manual Review**
   - Triggered if mandatory fields are missing
   - Triggered if the document cannot be parsed or has no extractable text

3. **Specialist Queue**
   - Triggered if the claim type is `injury`

4. **Fast-track**
   - Triggered if estimated damage is below 25,000

If none of the above conditions apply, the claim is routed for standard
processing.

---

## Project Structure

