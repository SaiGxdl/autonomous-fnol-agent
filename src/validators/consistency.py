from datetime import datetime
from typing import List
from validators.schema import ClaimData


def check_inconsistencies(claim: ClaimData) -> List[str]:
    """
    Returns a list of detected inconsistencies.
    """
    issues = []

    # Incident date in the future
    if claim.incident_info.date:
        try:
            incident_date = datetime.fromisoformat(claim.incident_info.date)
            if incident_date > datetime.now():
                issues.append("Incident date is in the future.")
        except ValueError:
            pass  # Ignore invalid date formats for now

    # Policy effective date after incident date
    if claim.policy_info.effective_date and claim.incident_info.date:
        try:
            policy_date = datetime.fromisoformat(claim.policy_info.effective_date)
            incident_date = datetime.fromisoformat(claim.incident_info.date)
            if policy_date > incident_date:
                issues.append("Policy effective date is after incident date.")
        except ValueError:
            pass

    # Damage described but estimate is zero
    if (
        claim.asset_info.damage_description
        and claim.asset_info.estimated_damage == 0
    ):
        issues.append("Damage described but estimated damage is zero.")

    return issues
