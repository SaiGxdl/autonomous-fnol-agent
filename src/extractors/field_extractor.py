import re
from validators.schema import (
    ClaimData,
    PolicyInfo,
    IncidentInfo,
    AssetInfo,
    InvolvedParty,
)
from utils.config import get_openai_api_key


def extract_with_rules(text: str) -> ClaimData:
    """
    Improved rule-based extraction for FNOL text.
    """
    
    def search(pattern):
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if not match:
            return None
        
        value=match.group(1).strip()
        blacklist = ["acord", "page", "©", "copyright"]
        if any(bad_word in value.lower() for bad_word in blacklist):
            return None
        return value if value else None
       

    policy_info = PolicyInfo(
        policy_number=search(r"POLICY NUMBER:\s*(.+)"),
        policyholder_name=search(r"NAME OF INSURED:\s*(.+)"),
    )

    incident_info = IncidentInfo(
        date = search(r"DATE OF LOSS:\s*([\d]{2}/[\d]{2}/[\d]{4})"),
        time=search(r"TIME:\s*([0-9:APM]+)"),
        location=search(r"LOCATION OF LOSS:\s*(.+)"),
        description=search(
            r"DESCRIPTION OF ACCIDENT:\s*([\s\S]*?)(?:\n\n|$)"
        ),
    )

    asset_info = AssetInfo(
        asset_type="vehicle",
        asset_id=search(r"VIN:\s*(\S+)"),
        estimated_damage=float(
            search(r"ESTIMATE AMOUNT:\s*(\d+)") or 0
        ),
        damage_description=search(r"DESCRIBE DAMAGE:\s*(.+)"),
    )

    claim_type = search(r"CLAIM TYPE:\s*(\w+)") or "auto"

    return ClaimData(
        policy_info=policy_info,
        incident_info=incident_info,
        asset_info=asset_info,
        claim_type=claim_type.lower(),
        attachments_present=False,
        initial_estimate=asset_info.estimated_damage,
        claimant=InvolvedParty(
            name=policy_info.policyholder_name
        ),
    )


def extract_fields(text: str) -> ClaimData:
    """
    Entry point for field extraction.

    If an OpenAI API key exists, an LLM-based extractor could be used.
    For this assessment, we intentionally default to deterministic
    rule-based extraction to ensure offline, reproducible execution.
    """
    _ = get_openai_api_key()  # intentionally unused (future extension)
    return extract_with_rules(text)
