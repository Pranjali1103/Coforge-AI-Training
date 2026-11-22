from pydantic import BaseModel
from typing import Literal

class ITSupportAnalysis(BaseModel):
    issue_category: Literal[
        "VPN",
        "Network",
        "Hardware",
        "Software",
        "Email",
        "Other"]

    priority_level: Literal[
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    suspected_root_cause: str

    impact_level: Literal[
        "Individual",
        "Team",
        "Organization"
    ]

    troubleshooting_steps: list[str]

    estimated_resolution_time: str | None = None

    