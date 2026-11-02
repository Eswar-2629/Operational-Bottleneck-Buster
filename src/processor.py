import csv
from datetime import date
from pathlib import Path

from models import Candidate, ProcessedCandidate

REQUIRED_FIELDS = [
    "employee_id", "full_name", "email", "department", "start_date",
    "employment_type", "offer_signed", "identity_document",
    "background_check", "bank_details",
]
BOOLEAN_FIELDS = ["offer_signed", "identity_document", "background_check", "bank_details"]
DOCUMENT_LABELS = {
    "offer_signed": "Offer signed",
    "identity_document": "Identity document",
    "background_check": "Background check",
    "bank_details": "Bank details",
}


class InputError(ValueError):
    pass


def parse_bool(value: str, field: str, row_number: int) -> bool:
    normalized = value.strip().lower()
    if normalized not in {"yes", "no"}:
        raise InputError(f"Row {row_number}: {field} must be 'yes' or 'no', got '{value}'")
    return normalized == "yes"


def load_candidates(path: str):
    source = Path(path)
    if not source.exists():
        raise InputError(f"Input file not found: {path}")

    candidates = []
    errors = []
    with source.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise InputError("Input CSV has no header row")

        missing_headers = [field for field in REQUIRED_FIELDS if field not in reader.fieldnames]
        if missing_headers:
            raise InputError("Missing required columns: " + ", ".join(missing_headers))

        for row_number, row in enumerate(reader, start=2):
            try:
                for field in REQUIRED_FIELDS:
                    if row.get(field) is None or not row[field].strip():
                        raise InputError(f"Row {row_number}: {field} is required")

                try:
                    parsed_date = date.fromisoformat(row["start_date"].strip())
                except ValueError:
                    raise InputError(
                        f"Row {row_number}: start_date must use YYYY-MM-DD"
                    )

                if "@" not in row["email"] or "." not in row["email"]:
                    raise InputError(f"Row {row_number}: invalid email address")

                candidates.append(Candidate(
                    employee_id=row["employee_id"].strip(),
                    full_name=row["full_name"].strip(),
                    email=row["email"].strip(),
                    department=row["department"].strip(),
                    start_date=parsed_date.isoformat(),
                    employment_type=row["employment_type"].strip(),
                    offer_signed=parse_bool(row["offer_signed"], "offer_signed", row_number),
                    identity_document=parse_bool(row["identity_document"], "identity_document", row_number),
                    background_check=parse_bool(row["background_check"], "background_check", row_number),
                    bank_details=parse_bool(row["bank_details"], "bank_details", row_number),
                ))
            except InputError as exc:
                errors.append({"row": row_number, "error": str(exc)})

    return candidates, errors


def classify(candidate: Candidate, as_of: date):
    start_date = date.fromisoformat(candidate.start_date)
    days_until_start = (start_date - as_of).days
    if days_until_start <= 7:
        priority = "Urgent"
    elif days_until_start <= 14:
        priority = "High"
    else:
        priority = "Standard"

    missing = []
    for field, label in DOCUMENT_LABELS.items():
        if not getattr(candidate, field):
            missing.append(label)

    if not missing:
        status = "Ready"
    elif "Background check" in missing or "Identity document" in missing:
        status = "Blocked"
    else:
        status = "Needs follow-up"

    return ProcessedCandidate(
        employee_id=candidate.employee_id,
        full_name=candidate.full_name,
        department=candidate.department,
        start_date=candidate.start_date,
        priority=priority,
        status=status,
        missing_items=tuple(missing),
    )
