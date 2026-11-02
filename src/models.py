from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Candidate:
    employee_id: str
    full_name: str
    email: str
    department: str
    start_date: str
    employment_type: str
    offer_signed: bool
    identity_document: bool
    background_check: bool
    bank_details: bool


@dataclass(frozen=True)
class ProcessedCandidate:
    employee_id: str
    full_name: str
    department: str
    start_date: str
    priority: str
    status: str
    missing_items: tuple

    def to_dict(self):
        result = asdict(self)
        result["missing_items"] = list(self.missing_items)
        return result
