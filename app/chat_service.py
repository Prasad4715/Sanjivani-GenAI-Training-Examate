
"""Chat service connecting legal record search, prompts, and Gemini."""

import json
import re
from pathlib import Path

from app.llm import LLMProvider
from app.records import get_by_id
from app.smart_search import smart_search


PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = PROJECT_ROOT / "prompts"


def load_prompt(filename: str) -> str:
    """Load a prompt from the prompts directory."""
    return (PROMPTS_DIR / filename).read_text(encoding="utf-8")


def find_relevant_records(question: str, limit: int = 3) -> list[dict]:
    """Find records using explicit section numbers and TF-IDF search."""
    records = []
    seen_sections = set()

    # Explicit section references take priority.
    section_numbers = re.findall(
        r"\b(?:section|sec\.?)\s*(\d+[A-Za-z]?)\b",
        question,
        flags=re.IGNORECASE,
    )

    for section in section_numbers:
        record = get_by_id(section.upper())

        if record and record["section"] not in seen_sections:
            records.append(record)
            seen_sections.add(record["section"])

    # Add relevant keyword matches.
    for record in smart_search(question, limit=limit):
        if record["section"] not in seen_sections:
            records.append(record)
            seen_sections.add(record["section"])

        if len(records) >= limit:
            break

    return records


def generate_chat_answer(question: str, prompt_version: str = "v2") -> dict:
    """Generate a grounded answer using legal records and Gemini."""
    if prompt_version not in {"v1", "v2"}:
        raise ValueError("Prompt version must be 'v1' or 'v2'.")

    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    records = find_relevant_records(question)

    if not records:
        return {
            "answer": "I don't have enough verified legal information to answer this question.",
            "confidence": "low",
            "follow_up": "Can you provide the Motor Vehicles Act section number from your challan?",
        }

    context = json.dumps(records, ensure_ascii=False, indent=2)

    task_prompt = load_prompt(f"task_{prompt_version}.txt")
    system_prompt = load_prompt("system.txt")

    prompt = task_prompt.replace("{question}", question).replace(
        "{context}", context
    )

    llm = LLMProvider()
    answer = llm.generate(prompt, system_prompt=system_prompt)

    uncertainty_phrases = (
        "i do not have enough verified information",
        "i don't have enough verified information",
        "i cannot verify",
        "i can't verify",
        "cannot be verified",
        "not enough information",
    )

    answer_indicates_uncertainty = any(
        phrase in answer.lower()
        for phrase in uncertainty_phrases
    )

    confidence = "low" if answer_indicates_uncertainty else "medium"

    return {
        "answer": answer,
        "confidence": confidence,
        "follow_up": (
            "Would you like help identifying the relevant official source?"
            if confidence == "low"
            else "Would you like an explanation of another section from your challan?"
        ),
    }
