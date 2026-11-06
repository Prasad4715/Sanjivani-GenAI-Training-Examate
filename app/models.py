
from dataclasses import dataclass
from typing import Optional


@dataclass
class Record:
    section: str
    offence: str
    max_fine_first: Optional[int]
    max_fine_repeat: Optional[int]
    other_action: str
    source_url: str

    # Additional fields from our ingestion pipeline
    legal_text: Optional[str] = None
    category: Optional[str] = None
