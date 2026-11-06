
from data.sample_records import sample_records


# 1. Load all traffic records
def load_records():
    return sample_records


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
