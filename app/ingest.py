
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

        with pymupdf.open(PDF_PATH) as pdf:

            all_text = []

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

    # The actual provision contains the footnote marker 1[177.
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

        # Match statutory section headings, including
        # headings with footnote markers such as 1[177.
        heading_pattern = re.compile(
            r"(?m)^[ \t]*(?:\d+\[)?(\d{3}[A-Z]?)\.[ \t]+"
        )

        matches = list(heading_pattern.finditer(chapter_text))

        section_match = None

        for match in matches:

            if match.group(1) == section_number:
                section_match = match
                break

        if section_match is None:
            raise ValueError(
                f"Section {section_number} not found."
            )

        start = section_match.start()

        # Remove a leading footnote marker from the text.
        heading_start = section_match.start(1)

        # Include the section number, but not the footnote.
        start = heading_start

        end = len(chapter_text)

        # Find the next statutory section heading.
        for match in matches:

            if match.start() > section_match.start():
                end = match.start()
                break

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
# STEP 4: CLEAN SECTION DATA
# --------------------------------------------------

def clean_section(section_number, section_text):

    try:

        if not section_text:
            raise ValueError("Section text is empty.")

        # Normalize whitespace without changing wording.
        legal_text = re.sub(
            r"\s+",
            " ",
            section_text
        ).strip()

        # Extract offence heading up to the statutory dash.
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

        record = {
            "section": section_number,
            "offence": offence,
            "max_fine_first": None,
            "max_fine_repeat": None,
            "other_action": (
                "Refer to the complete statutory text "
                "for applicable penalties and consequences."
            ),
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
# STEP 5: SAVE JSON DATA
# --------------------------------------------------

def save_records(records):

    try:

        OUTPUT_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            OUTPUT_PATH,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                records,
                file,
                indent=4,
                ensure_ascii=False
            )

        print("\nSuccessfully saved", len(records), "records.")
        print("Output File:", OUTPUT_PATH)

    except Exception as error:

        print("JSON Save Error:", error)


# --------------------------------------------------
# STEP 6: MAIN INGESTION PIPELINE
# --------------------------------------------------

def ingest():

    print("\nStarting ChalanCheck Data Ingestion...\n")

    all_text = extract_pdf_text()

    if not all_text:
        print("No PDF text available. Ingestion stopped.")
        return

    records = []
    failed_sections = []

    for section_number in TARGET_SECTIONS:

        print(f"Processing Section {section_number}...")

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

    save_records(records)

    print("\nIngestion Summary")
    print("-----------------")
    print("Target Sections:", len(TARGET_SECTIONS))
    print("Successfully Extracted:", len(records))
    print("Failed:", len(failed_sections))

    if failed_sections:
        print("Failed Sections:", failed_sections)


if __name__ == "__main__":
    ingest()
