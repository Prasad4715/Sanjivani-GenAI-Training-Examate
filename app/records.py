
from data.sample_records import sample_records


# 1. Load all traffic records
import json
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "records.json"


def load_records():
    """Load structured traffic challan records from JSON."""
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            records = json.load(file)

        if not isinstance(records, list):
            raise ValueError("Expected a list of records in records.json")

        return records

    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise RuntimeError(f"Unable to load ChalanCheck records: {error}") from error


# 2. Search records using a keyword

def search(keyword):
    keyword = keyword.lower().strip()

    # Common words used by vehicle owners
    synonyms = {
        "helmet": "headgear",
        "seatbelt": "safety belt",
        "speeding": "speed limits",
        "drunk driving": "alcohol"
    }

    search_keyword = synonyms.get(keyword, keyword)

    results = []

    for record in load_records():

        text = (
            record["offence"] + " " +
            record["other_action"] + " " +
            record["section"]
        ).lower()

        if keyword in text or search_keyword in text:
            results.append(record)

    return results



# 3. Count records by category
def count_by(field):
    counts = {}

    for record in load_records():
        value = record.get(field)

        if value is not None:
            counts[value] = counts.get(value, 0) + 1

    return counts


# 4. Find a record using section number
def get_by_id(section):
    for record in load_records():

        if record["section"] == str(section):
            return record

    return None
