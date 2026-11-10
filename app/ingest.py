
import re
import json
from pathlib import Path

import pymupdf


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_PATH = BASE_DIR / "data" / "raw" / "motor_vehicles_act_1988.pdf"
OUTPUT_PATH = BASE_DIR / "data" / "records.json"

SOURCE_URL = (
    "https://www.indiacode.nic.in/bitstream/"
    "123456789/1798/1/A1988-59.pdf"
)

TARGET_SECTIONS = [
    "177", "179", "180", "181", "182",
    "183", "184", "185", "186", "189",
    "190", "192", "192A", "194", "194A",
    "194B", "194C", "194D", "194E", "196"
]


# --------------------------------------------------
# STEP 1: EXTRACT PDF TEXT
# --------------------------------------------------

def extract_pdf_text():
    try:
        if not PDF_PATH.exists():
            raise FileNotFoundError(
                f"PDF file not found: {PDF_PATH}"
            )

        all_text = []

        with pymupdf.open(PDF_PATH) as pdf:
            print("Total PDF Pages:", len(pdf))

            for page_number, page in enumerate(pdf, start=1):
                try:
                    text = page.get_text()

                    if text.strip():
                        all_text.append(text)

                except Exception as error:
                    print(
                        f"Error reading page {page_number}: {error}"
                    )

        return "\n".join(all_text)

    except Exception as error:
        print("PDF Extraction Error:", error)
        return None


# --------------------------------------------------
# STEP 2: FIND ACTUAL SECTION 177
# --------------------------------------------------

def find_chapter_start(all_text):
    pattern = re.compile(
        r"(?m)^[ \t]*\d+\[177\.[ \t]+"
    )

    match = pattern.search(all_text)

    if match:
        return match.start()

    raise ValueError(
        "Actual Section 177 heading not found."
    )


# --------------------------------------------------
# STEP 3: EXTRACT INDIVIDUAL SECTION
# --------------------------------------------------

def extract_section(all_text, section_number):
    try:
        chapter_start = find_chapter_start(all_text)
        chapter_text = all_text[chapter_start:]

        # Supports normal and amended headings.
        heading_pattern = re.compile(
            r"(?m)^[ \t]*(?:\d+\s*)?\[?\s*"
            r"(\d{3}[A-Z]?)\.\s+"
        )

        matches = list(heading_pattern.finditer(chapter_text))

        section_match = None
        section_index = None

        for index, match in enumerate(matches):
            if match.group(1) == section_number:
                section_match = match
                section_index = index
                break

        if section_match is None:
            raise ValueError(
                f"Section {section_number} not found."
            )

        start = section_match.start(1)

        if section_index + 1 < len(matches):
            end = matches[section_index + 1].start()
        else:
            end = len(chapter_text)

        section_text = chapter_text[start:end].strip()

        if not section_text:
            raise ValueError(
                f"Section {section_number} has empty text."
            )

        return section_text

    except Exception as error:
        print(
            f"Section {section_number} Extraction Error: {error}"
        )
        return None


# --------------------------------------------------
# STEP 4: CLEAN PDF TEXT
# --------------------------------------------------

def clean_legal_text(text):

    # Remove PDF page headers and footers.
    text = re.sub(
        r"(?im)^[ \t]*IndiaCode[ \t]*$",
        "",
        text
    )

    text = re.sub(
        r"(?m)^[ \t]*\d{1,3}[ \t]*$",
        "",
        text
    )

    # Remove amendment footnote lines.
    text = re.sub(
        r"(?im)^[ \t]*\d+\.\s+"
        r"(?:Subs\.|Ins\.|Omitted|Added|Inserted|Amended|See)"
        r"[^\n]*(?:\n|$)",
        "",
        text
    )

    # Restore spaces between joined words.
    text = re.sub(
        r"(?<=[a-z])(?=[A-Z])",
        " ",
        text
    )

    # Normalize whitespace.
    text = re.sub(r"\s+", " ", text).strip()

    return text


# --------------------------------------------------
# STEP 5: WORD TO NUMBER CONVERSION
# --------------------------------------------------

NUMBER_WORDS = {
    "one hundred": 100,
    "two hundred": 200,
    "three hundred": 300,
    "five hundred": 500,
    "one thousand": 1000,
    "one thousand and five hundred": 1500,
    "fifteen hundred": 1500,
    "two thousand": 2000,
    "twenty-five hundred": 2500,
    "five thousand": 5000,
    "ten thousand": 10000,
    "fifteen thousand": 15000,
    "twenty thousand": 20000,
    "twenty-five thousand": 25000,
    "fifty thousand": 50000,
}


def word_to_number(text):
    normalized = text.lower().strip()
    return NUMBER_WORDS.get(normalized)


# --------------------------------------------------
# STEP 6: EXTRACT FINE AMOUNTS
# --------------------------------------------------

def extract_max_fine(text):
    values = []

    amount_words = "|".join(
        re.escape(word)
        for word in sorted(NUMBER_WORDS, key=len, reverse=True)
    )

    word_pattern = re.compile(
        rf"(?i)(?:fine|penalty)[^.;]{{0,150}}?"
        rf"(?:of\s+)?({amount_words})\s+rupees"
    )

    for match in word_pattern.finditer(text):
        amount = word_to_number(match.group(1))

        if amount is not None:
            values.append(amount)

    numeric_pattern = re.compile(
        r"(?i)(?:fine|penalty)[^.;]{0,150}?"
        r"(?:₹|Rs\.?\s*)\s*([\d,]+)"
    )

    for match in numeric_pattern.finditer(text):
        try:
            values.append(
                int(match.group(1).replace(",", ""))
            )
        except ValueError:
            continue

    return max(values) if values else None


# --------------------------------------------------
# STEP 7: EXTRACT OTHER LEGAL CONSEQUENCES
# --------------------------------------------------

def extract_other_actions(text):
    actions = []

    # Warning.
    if re.search(r"\bwarning\b", text, re.IGNORECASE):
        actions.append(
            "Warning for first contravention"
        )

    # Imprisonment.
    imprisonment_matches = re.findall(
        r"imprisonment for a term which may extend to "
        r"[^,;.]+",
        text,
        flags=re.IGNORECASE
    )

    for item in imprisonment_matches:
        actions.append(item.strip())

    # Licence validity.
    if re.search(
        r"licence so obtained by him shall be of no effect",
        text,
        re.IGNORECASE
    ):
        actions.append(
            "Licence obtained is of no effect"
        )

    # Fine and imprisonment together.
    if re.search(
        r"\bor with both\b|\bor both\b",
        text,
        re.IGNORECASE
    ):
        actions.append(
            "Fine and imprisonment may both apply"
        )

    # Driving licence impounding.
    if re.search(
        r"\b(?:driving\s+)?licen[cs]e\b.{0,100}\bimpounded\b",
        text,
        re.IGNORECASE
    ):
        actions.append(
            "Driving licence impounding provisions apply"
        )

    # Driving disqualification.
    if re.search(
        r"disqualif",
        text,
        re.IGNORECASE
    ):
        actions.append(
            "Driving licence disqualification provisions apply"
        )

    if not actions:
        actions.append(
            "See legal_text for the statutory consequences."
        )

    return "; ".join(dict.fromkeys(actions))


# --------------------------------------------------
# STEP 8: CLEAN AND STRUCTURE A SECTION
# --------------------------------------------------

def clean_section(section_number, section_text):
    try:
        if not section_text:
            raise ValueError("Section text is empty.")

        legal_text = clean_legal_text(section_text)

        # Extract offence heading.
        heading_pattern = re.compile(
            rf"^{re.escape(section_number)}\.\s*(.*?)\s*[—–-]",
            re.DOTALL
        )

        heading_match = heading_pattern.search(legal_text)

        if heading_match:
            offence = heading_match.group(1).strip()
        else:
            offence = (
                f"Section {section_number} "
                "of the Motor Vehicles Act"
            )

        maximum_fine = extract_max_fine(legal_text)

        max_fine_first = None
        max_fine_repeat = None

        # Section 177: first warning, repeat fine.
        if section_number == "177":

            if re.search(
                r"first contravention.*?warning",
                legal_text,
                re.IGNORECASE
            ):
                max_fine_first = None

            repeat_match = re.search(
                r"second or subsequent contravention.*?"
                r"extend to\s+one thousand and five hundred rupees",
                legal_text,
                re.IGNORECASE
            )

            if repeat_match:
                max_fine_repeat = 1500

        # Section 183: speeding.
        elif section_number == "183":

            # Highest maximum across vehicle categories.
            max_fine_first = 4000

            # No separately stated repeat monetary fine.
            max_fine_repeat = None
            
        elif section_number == "184":

            # Dangerous driving: first offence.
            max_fine_first = 5000

            # Second or subsequent offence within three years.
            max_fine_repeat = 10000
        # Section 185: drunken driving.
        elif section_number == "185":

            max_fine_first = 10000
            max_fine_repeat = 15000

        elif section_number == "186":

            # First contravention maximum penalty.
            max_fine_first = 1000

            # Second or subsequent contravention maximum penalty.
            max_fine_repeat = 2000

        elif section_number == "189":

            # First offence: racing or trial of speed.
            max_fine_first = 5000

            # Subsequent offence.
            max_fine_repeat = 10000

        elif section_number == "190":

            # Highest first-offence amount across Section 190 subsections.
            max_fine_first = 10000

            # Highest subsequent-offence amount across Section 190 subsections.
            max_fine_repeat = 20000

        elif section_number == "192":

            # First offence: vehicle without registration.
            max_fine_first = 5000

            # Second or subsequent offence.
            max_fine_repeat = 10000
        # Other sections: current basic extraction.
        else:
            max_fine_first = maximum_fine

        other_action = extract_other_actions(legal_text)

        # Specific repeat-offence consequence.
        if section_number == "183" and re.search(
            r"second or any subsequent offence.*?"
            r"driving licence.*?impounded",
            legal_text,
            re.IGNORECASE
        ):
            other_action = (
                "Driving licence shall be impounded for "
                "a second or subsequent offence under "
                "Section 183, as provided in Section 206(4)."
            )

        record = {
            "section": section_number,
            "offence": offence,
            "max_fine_first": max_fine_first,
            "max_fine_repeat": max_fine_repeat,
            "other_action": other_action,
            "source_url": SOURCE_URL,
            "legal_text": legal_text
        }

        return record

    except Exception as error:
        print(
            f"Section {section_number} Cleaning Error: {error}"
        )
        return None


# --------------------------------------------------
# STEP 9: SAVE JSON DATA
# --------------------------------------------------

def save_records(records):
    try:
        OUTPUT_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        # Write to a temporary file first.
        temporary_path = OUTPUT_PATH.with_suffix(".json.tmp")

        with open(
            temporary_path,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                records,
                file,
                indent=4,
                ensure_ascii=False
            )

        # Replace the existing file after writing succeeds.
        temporary_path.replace(OUTPUT_PATH)

        print(
            "\nSuccessfully saved",
            len(records),
            "records."
        )
        print("Output File:", OUTPUT_PATH)

    except Exception as error:
        print("JSON Save Error:", error)


# --------------------------------------------------
# STEP 10: MAIN INGESTION PIPELINE
# --------------------------------------------------

def ingest():

    print("\nStarting ChalanCheck Data Ingestion...\n")

    all_text = extract_pdf_text()

    if not all_text:
        print(
            "No PDF text available. Ingestion stopped."
        )
        return

    records = []
    failed_sections = []

    for section_number in TARGET_SECTIONS:

        print(f"Processing Section {section_number}...")

        try:
            section_text = extract_section(
                all_text,
                section_number
            )

            if section_text is None:
                failed_sections.append(section_number)
                continue

            record = clean_section(
                section_number,
                section_text
            )

            if record is None:
                failed_sections.append(section_number)
                continue

            records.append(record)

        except Exception as error:
            print(
                f"Unexpected error in Section "
                f"{section_number}: {error}"
            )
            failed_sections.append(section_number)

    print("\nIngestion Summary")
    print("-----------------")
    print("Target Sections:", len(TARGET_SECTIONS))
    print("Successfully Extracted:", len(records))
    print("Failed:", len(failed_sections))

    if failed_sections or len(records) != len(TARGET_SECTIONS):
        print(
            "Incomplete extraction. "
            "Existing records.json has been preserved."
        )
        print("Failed Sections:", failed_sections)
        return

    save_records(records)


# --------------------------------------------------
# PROGRAM ENTRY POINT
# --------------------------------------------------

if __name__ == "__main__":
    ingest()
