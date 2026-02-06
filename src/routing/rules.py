from validators.schema import ClaimData, MANDATORY_FIELDS


FRAUD_KEYWORDS = {"fraud", "inconsistent", "staged"}


def get_nested_attr(obj, attr_path: str):
    for attr in attr_path.split("."):
        obj = getattr(obj, attr, None)
        if obj is None:
            return None
    return obj


def find_missing_fields(claim: ClaimData):
    missing = []
    for field_path in MANDATORY_FIELDS:
        if get_nested_attr(claim, field_path) in (None, "", []):
            missing.append(field_path.split(".")[-1])
    return missing


def determine_route(claim: ClaimData, missing_fields: list, inconsistencies: list):
    description = (
        claim.incident_info.description.lower()
        if claim.incident_info.description
        else ""
    )

    # 1️⃣ Missing mandatory fields (highest priority)
    if missing_fields:
        return (
            "Manual Review",
            f"Mandatory fields are missing: {missing_fields}",
        )

    # 2️⃣ Fraud keywords
    if any(word in description for word in FRAUD_KEYWORDS):
        return (
            "Investigation",
            "Fraud-related keywords detected in claim description.",
        )

    # 3️⃣ Injury claims
    if claim.claim_type and claim.claim_type.lower() == "injury":
        return (
            "Specialist Queue",
            "Injury-related claim requires specialist handling.",
        )

    # 4️⃣ Damage-based routing
    if (
        claim.asset_info.estimated_damage is not None
        and claim.asset_info.estimated_damage < 25000
    ):
        return (
            "Fast-track",
            "Estimated damage is below 25,000.",
        )

    return (
        "Standard Processing",
        "Claim does not meet any special routing criteria.",
    )

