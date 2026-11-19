
"""Tools for the ChalanCheck agent."""

import json
import re
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RECORDS_PATH = PROJECT_ROOT / "data" / "records.json"

UNKNOWN_ACTIONS = {
    "",
    "none",
    "n/a",
    "not specified",
    "see legal_text for the statutory consequences.",
}


def load_records() -> list[dict]:
    """Load and validate structured legal records."""

    if not RECORDS_PATH.is_file():
        raise FileNotFoundError(
            f"Legal records file not found: {RECORDS_PATH}"
        )

    with RECORDS_PATH.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError("records.json must contain a list.")

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(
                f"Record {index} must be a dictionary."
            )
        if not record.get("section"):
            raise ValueError(
                f"Record {index} has no section code."
            )

    return records


def normalize_section(section: str) -> str:
    """Normalize a section code such as 'Section 194d'."""

    if not isinstance(section, str):
        raise ValueError("Section codes must be strings.")

    value = section.strip().upper()

    value = re.sub(
        r"^(?:SECTION|SEC\.?)\s*",
        "",
        value,
        flags=re.IGNORECASE,
    )

    if not re.fullmatch(r"\d+[A-Z]?", value):
        raise ValueError(
            f"Invalid section code: {section!r}"
        )

    return value


def parse_fine(value: Any) -> int | None:
    """Read a non-negative fine without inventing values."""

    if value is None:
        return None

    if isinstance(value, bool):
        raise ValueError("Fine cannot be a boolean.")

    if isinstance(value, int):
        fine = value
    elif isinstance(value, str):
        cleaned = value.strip().replace(",", "")
        if not cleaned.isdigit():
            raise ValueError(
                f"Invalid fine value: {value!r}"
            )
        fine = int(cleaned)
    else:
        raise ValueError(
            f"Unsupported fine value: {value!r}"
        )

    if fine < 0:
        raise ValueError("Fine cannot be negative.")

    return fine


def challan_total_calculator(
    sections: list[str],
    repeat_offence: bool = False,
) -> dict:
    """
    Calculate the sum of recorded maximum fines.

    Missing fine values are reported as unknown.
    They are never silently treated as zero.
    """

    if not isinstance(sections, list) or not sections:
        raise ValueError(
            "Provide a non-empty list of section codes."
        )

    if not isinstance(repeat_offence, bool):
        raise ValueError(
            "repeat_offence must be True or False."
        )

    normalized_sections = list(
        dict.fromkeys(
            normalize_section(section)
            for section in sections
        )
    )

    records = load_records()

    record_lookup = {
        normalize_section(record["section"]): record
        for record in records
    }

    fine_field = (
        "max_fine_repeat"
        if repeat_offence
        else "max_fine_first"
    )

    total_known_fines = 0
    fine_breakdown = []
    consequences = []
    unknown_sections = []
    missing_fines = []

    for section in normalized_sections:
        record = record_lookup.get(section)

        if record is None:
            unknown_sections.append(section)
            continue

        fine = parse_fine(record.get(fine_field))

        if fine is None:
            missing_fines.append(section)
        else:
            total_known_fines += fine

        action = record.get("other_action")

        if isinstance(action, str):
            action = action.strip()

            if action.lower() not in UNKNOWN_ACTIONS:
                first_only_warning = (
                    repeat_offence
                    and "warning for first contravention" in action.lower()
                )

                if not first_only_warning:
                    consequences.append({
                        "section": section,
                        "action": action,
                    })


        fine_breakdown.append({
            "section": section,
            "offence": record.get("offence", ""),
            "maximum_fine": fine,
            "other_action": action,
            "source_url": record.get("source_url", ""),
        })

    complete = (
        not unknown_sections
        and not missing_fines
    )

    return {
        "requested_sections": normalized_sections,
        "repeat_offence": repeat_offence,
        "total_maximum_fine": (
            total_known_fines if complete else None
        ),
        "known_fines_subtotal": total_known_fines,
        "currency": "INR",
        "fine_breakdown": fine_breakdown,
        "non_money_consequences": consequences,
        "unknown_sections": unknown_sections,
        "missing_fine_sections": missing_fines,
        "complete": complete,
        "note": (
            "Sum of recorded statutory maximum fines; "
            "not an official payable challan amount. "
            "Missing values are not treated as zero. "
            "Additional actions are taken from records.json "
            "and require legal verification."
        ),
    }


if __name__ == "__main__":
    result = challan_total_calculator(
        sections=["180", "181"],
        repeat_offence=False,
    )

    print(json.dumps(result, indent=2))
