
"""Hand-written tool-calling agent for ChalanCheck."""

import json
import re
from typing import Any

from app.rag import ask_question
from app.tools import challan_total_calculator

MAX_TOOL_CALLS = 3


def extract_section_codes(question: str) -> list[str]:
    """Extract explicitly mentioned legal section codes."""

    pattern = (
        r"\b(?:sections?|sec\.?)\s*"
        r"(\d+[A-Za-z]?"
        r"(?:\s*(?:,|/|&|and)\s*\d+[A-Za-z]?)*)"
    )

    sections = []

    for match in re.finditer(
        pattern,
        question,
        flags=re.IGNORECASE,
    ):
        found = re.findall(
            r"\d+[A-Za-z]?",
            match.group(1),
        )
        sections.extend(found)

    return list(
        dict.fromkeys(
            section.upper()
            for section in sections
        )
    )



def detect_repeat_offence(question: str) -> bool:
    """Detect an explicitly mentioned repeat traffic offence."""

    return bool(
        re.search(
            r"\b("
            r"repeat(?:ed)?\s+(?:traffic\s+)?offen[cs]e"
            r"|second\s+(?:traffic\s+)?offen[cs]e"
            r"|subsequent\s+(?:traffic\s+)?offen[cs]e"
            r"|second\s+contravention"
            r"|subsequent\s+contravention"
            r"|offen[cs]e\s+(?:committed\s+)?again"
            r")\b",
            question,
            flags=re.IGNORECASE,
        )
    )



def select_tools(question: str) -> list[str]:
    """Choose the tools needed to answer the question."""

    lower = question.lower()

    calculation_keywords = (
        "total fine",
        "total penalty",
        "combined fine",
        "combined penalty",
        "calculate",
        "sum of fines",
        "maximum total",
        "add the fines",
    )

    explanation_keywords = (
        "explain",
        "what does",
        "why",
        "how",
        "punishment",
        "consequences",
        "disqualification",
        "refresher",
    )

    needs_calculator = any(
        keyword in lower
        for keyword in calculation_keywords
    )

    needs_explanation = any(
        keyword in lower
        for keyword in explanation_keywords
    )

    if needs_calculator and needs_explanation:
        return ["calculator", "rag"]

    if needs_calculator:
        return ["calculator"]

    return ["rag"]


def run_agent(
    question: str,
    top_k: int = 5,
    max_tool_calls: int = MAX_TOOL_CALLS,
) -> dict[str, Any]:
    """
    Execute a small, deterministic agent loop.

    The agent chooses tools, executes them and combines
    the results without inventing legal information.
    """

    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question cannot be empty.")

    if not 1 <= top_k <= 20:
        raise ValueError("top_k must be between 1 and 20.")

    if max_tool_calls < 1:
        raise ValueError(
            "max_tool_calls must be positive."
        )

    selected_tools = select_tools(question)

    sections = extract_section_codes(question)
    repeat_offence = detect_repeat_offence(question)

    tool_results = {}
    tool_calls = []
    errors = []

    pending_tools = list(selected_tools)

    while pending_tools and len(tool_calls) < max_tool_calls:
        tool_name = pending_tools.pop(0)

        try:
            if tool_name == "calculator":
                if not sections:
                    errors.append(
                        "Cannot calculate a fine without "
                        "explicit section codes."
                    )
                    continue

                result = challan_total_calculator(
                    sections=sections,
                    repeat_offence=repeat_offence,
                )

            elif tool_name == "rag":
                result = ask_question(
                    question=question,
                    top_k=top_k,
                )

            else:
                errors.append(
                    f"Unknown tool: {tool_name}"
                )
                continue

            tool_results[tool_name] = result
            tool_calls.append(tool_name)

        except Exception as exc:
            errors.append(
                f"{tool_name} failed: "
                f"{type(exc).__name__}: {exc}"
            )
            tool_calls.append(tool_name)

    answer_parts = []

    calculator_result = tool_results.get("calculator")

    if calculator_result:
        total = calculator_result["total_maximum_fine"]
        subtotal = calculator_result["known_fines_subtotal"]

        if total is not None:
            answer_parts.append(
                f"Maximum recorded fine total: ₹{total:,}."
            )
        else:
            answer_parts.append(
                "A complete maximum fine total cannot "
                "be determined from the available records. "
                f"Known fines subtotal: ₹{subtotal:,}."
            )

        for item in calculator_result["fine_breakdown"]:
            fine = item["maximum_fine"]

            fine_text = (
                f"₹{fine:,}"
                if fine is not None
                else "not available in records"
            )

            answer_parts.append(
                f"Section {item['section']}: {fine_text}"
            )

        consequences = calculator_result[
            "non_money_consequences"
        ]

        if consequences:
            answer_parts.append(
                "Additional recorded consequences:"
            )

            for item in consequences:
                answer_parts.append(
                    f"Section {item['section']}: "
                    f"{item['action']}"
                )

        if calculator_result["unknown_sections"]:
            answer_parts.append(
                "Unknown sections: "
                + ", ".join(
                    calculator_result["unknown_sections"]
                )
            )

        answer_parts.append(calculator_result["note"])

    rag_result = tool_results.get("rag")

    if rag_result:
        answer_parts.append(
            rag_result["answer"]
        )

    if not answer_parts:
        answer_parts.append(
            "I could not complete the request "
            "using the available tools."
        )

    return {
        "question": question,
        "answer": "\n\n".join(answer_parts),
        "sections": sections,
        "repeat_offence": repeat_offence,
        "tools_used": tool_calls,
        "tool_results": tool_results,
        "errors": errors,
        "citations": (
            rag_result.get("citations", [])
            if rag_result
            else []
        ),
    }


if __name__ == "__main__":
    question = (
        "Calculate the maximum total fine "
        "for Sections 180 and 181."
    )

    result = run_agent(question)

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False,
        )
    )
