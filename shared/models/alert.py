from dataclasses import dataclass


@dataclass
class Alert:
    type: str
    severity: str
    details: dict

