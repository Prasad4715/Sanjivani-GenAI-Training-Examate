
from dataclasses import dataclass


@dataclass
class Record:
    section: str
    offence: str
    max_fine_first: int | None
    max_fine_repeat: int | None
    other_action: str
    source_url: str

    # Additional fields from our ingestion pipeline
    legal_text: str | None = None
    category: str | None = None
