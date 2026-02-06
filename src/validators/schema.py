from pydantic import BaseModel, Field
from typing import Optional, List


class PolicyInfo(BaseModel):
    policy_number: Optional[str] = None
    policyholder_name: Optional[str] = None
    effective_date: Optional[str] = None


class IncidentInfo(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None


class InvolvedParty(BaseModel):
    name: Optional[str] = None
    contact_details: Optional[str] = None


class AssetInfo(BaseModel):
    asset_type: Optional[str] = None
    asset_id: Optional[str] = None
    estimated_damage: Optional[float] = None
    damage_description: Optional[str] = None


class ClaimData(BaseModel):
    policy_info: PolicyInfo
    incident_info: IncidentInfo
    claimant: Optional[InvolvedParty] = None
    third_parties: Optional[List[InvolvedParty]] = []
    asset_info: AssetInfo
    claim_type: Optional[str] = None
    attachments_present: Optional[bool] = None
    initial_estimate: Optional[float] = None


MANDATORY_FIELDS = [
    "policy_info.policy_number",
    "policy_info.policyholder_name",
    "incident_info.date",
    "incident_info.location",
    "incident_info.description",
]

