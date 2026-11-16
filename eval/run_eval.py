
"""Evaluate ChalanCheck RAG across two retrieval configurations."""

import json
import re
import time
from pathlib import Path

from app.rag import ask_question


ROOT = Path(__file__).resolve().parent
EVAL_FILE = ROOT / "eval_set.json"
RESULTS_FILE = ROOT / "rag_eval_results.json"
REPORT_FILE = ROOT / "rag_eval_report.md"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 250

CONFIGS = {
    "A_top3": {"top_k": 3},
    "B_top5": {"top_k": 5},
}

REQUEST_DELAY = 5
MAX_ATTEMPTS = 4



def normalize(text: str) -> str:
    """Normalize numbers and text for approximate matching."""

    text = text.lower().replace(",", "")

    # Normalize equivalent legal terms.
    synonyms = {
        "protective headgear": "helmet",
        "motor cycle": "motorcycle",
        "uninsured": "insurance",
        "authorities": "authority",
        "impounded": "impound",
        "disqualification": "disqualification",
    }

    for original, replacement in synonyms.items():
        text = re.sub(
            rf"\b{re.escape(original)}\b",
            replacement,
            text,
        )


    number_words = {
        "one thousand": "1000",
        "two thousand": "2000",
        "three thousand": "3000",
        "four thousand": "4000",
        "five thousand": "5000",
        "ten thousand": "10000",
        "fifteen thousand": "15000",
    }

    for words, digits in sorted(
        number_words.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        text = re.sub(
            rf"\b{re.escape(words)}\b",
            digits,
            text,
        )

    text = re.sub(r"[^a-z0-9]+", " ", text)

    return " ".join(text.split())



def evaluate_answer(item: dict, result: dict) -> dict:
    """Score an answer using automated checks."""

    answer = result["answer"]
    normalized_answer = normalize(answer)

    abstained = answer.strip().lower() == "i don't know"
    expected_abstention = item["should_abstain"]

    if expected_abstention:
        passed = abstained and not result["citations"]

        return {
            "passed": passed,
            "abstained": abstained,
            "keyword_score": None,
            "section_score": None,
            "has_citations": bool(result["citations"]),
        }

    keywords = item["expected_keywords"]
    sections = item["expected_sections"]

    keyword_hits = sum(
        normalize(keyword) in normalized_answer
        for keyword in keywords
    )

    section_hits = sum(
        bool(
            re.search(
                rf"\b{re.escape(section.lower())}\b",
                answer.lower(),
            )
        )
        for section in sections
    )

    keyword_score = (
        keyword_hits / len(keywords)
        if keywords else 1.0
    )

    section_score = (
        section_hits / len(sections)
        if sections else 1.0
    )

    has_citations = bool(result["citations"])

    passed = (
        not abstained
        and keyword_score == 1.0
        and section_score == 1.0
        and has_citations
    )

    return {
        "passed": passed,
        "abstained": abstained,
        "keyword_score": keyword_score,
        "section_score": section_score,
        "has_citations": has_citations,
    }


def is_temporary_error(exc: Exception) -> bool:
    """Detect temporary Gemini rate-limit or availability errors."""

    error_text = str(exc).lower()

    return any(
        term in error_text
        for term in (
            "429",
            "resource_exhausted",
            "rate limit",
            "503",
            "unavailable",
        )
    )


def ask_with_retry(question: str, top_k: int) -> dict:
    """Retry temporary API errors with increasing delays."""

    for attempt in range(MAX_ATTEMPTS):
        try:
            return ask_question(
                question=question,
                top_k=top_k,
            )

        except Exception as exc:
            if (
                not is_temporary_error(exc)
                or attempt == MAX_ATTEMPTS - 1
            ):
                raise

            wait_seconds = 15 * (attempt + 1)

            print(
                f"    Temporary API error. "
                f"Waiting {wait_seconds}s before retry "
                f"{attempt + 2}/{MAX_ATTEMPTS}...",
                flush=True,
            )

            time.sleep(wait_seconds)

    raise RuntimeError("All retry attempts failed.")


def run_evaluation():
    """Run both configurations and generate evaluation reports."""

    with EVAL_FILE.open(encoding="utf-8") as file:
        dataset = json.load(file)

    all_results = {}
    summary = []

    for config_name, config in CONFIGS.items():
        print(f"\nRunning {config_name}...")

        config_results = []

        passed_count = 0
        api_error_count = 0
        total_time = 0.0
        successful_time = 0.0

        for item in dataset:
            time.sleep(REQUEST_DELAY)

            print(
                f"  {item['id']}: {item['question']}",
                flush=True,
            )

            start = time.perf_counter()

            try:
                result = ask_with_retry(
                    question=item["question"],
                    top_k=config["top_k"],
                )

                elapsed = time.perf_counter() - start

                total_time += elapsed
                successful_time += elapsed

                scores = evaluate_answer(item, result)

                if scores["passed"]:
                    passed_count += 1

                config_results.append({
                    "id": item["id"],
                    "question": item["question"],
                    "answer": result["answer"],
                    "citations": result["citations"],
                    "retrieved_chunks": result["retrieved_chunks"],
                    "time_seconds": round(elapsed, 2),
                    "scores": scores,
                })

                status = "PASS" if scores["passed"] else "FAIL"
                print(f"    Result: {status}", flush=True)

            except Exception as exc:
                elapsed = time.perf_counter() - start
                total_time += elapsed

                api_error_count += 1

                print(
                    f"    ERROR: {type(exc).__name__}: {exc}",
                    flush=True,
                )

                config_results.append({
                    "id": item["id"],
                    "question": item["question"],
                    "error": str(exc),
                    "time_seconds": round(elapsed, 2),
                    "scores": {"passed": False},
                })

        total_questions = len(dataset)

        valid_questions = total_questions - api_error_count

        valid_pass_rate = (
            passed_count / valid_questions * 100
            if valid_questions else 0.0
        )

        average_time = (
            successful_time / valid_questions
            if valid_questions else 0.0
        )

        summary.append({
            "configuration": config_name,
            "top_k": config["top_k"],
            "chunk_size": CHUNK_SIZE,
            "chunk_overlap": CHUNK_OVERLAP,
            "passed": passed_count,
            "total": total_questions,
            "api_errors": api_error_count,
            "valid_questions": valid_questions,
            "pass_rate": round(valid_pass_rate, 2),
            "average_time_seconds": round(average_time, 2),
            "total_time_seconds": round(total_time, 2),
        })

        all_results[config_name] = config_results

    RESULTS_FILE.write_text(
        json.dumps(
            {
                "summary": summary,
                "results": all_results,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    # Only declare a winner if both configurations completed
    # every evaluation without API errors.
    comparison_complete = all(
        row["api_errors"] == 0
        for row in summary
    )

    if comparison_complete:
        winner = sorted(
            summary,
            key=lambda row: (
                -row["pass_rate"],
                row["average_time_seconds"],
            ),
        )[0]

        winner_text = winner["configuration"]

    else:
        winner_text = "Pending — API errors affected the comparison"

    report = [
        "# Day 8 — RAG Evaluation Results",
        "",
        "## Configuration Comparison",
        "",
        f"Chunk size: {CHUNK_SIZE} characters",
        "",
        f"Chunk overlap: {CHUNK_OVERLAP} characters",
        "",
        "| Configuration | Top-k | Passed | API Errors | Pass Rate | Avg Time |",
        "|---|---:|---:|---:|---:|---:|",
    ]

    for row in summary:
        report.append(
            f"| {row['configuration']} "
            f"| {row['top_k']} "
            f"| {row['passed']}/{row['valid_questions']} "
            f"| {row['api_errors']} "
            f"| {row['pass_rate']}% "
            f"| {row['average_time_seconds']}s |"
        )

    report.extend([
        "",
        f"**Winner:** {winner_text}",
        "",
        "## Evaluation Method",
        "",
        "- Both configurations use the same PDF chunks.",
        "- Config A retrieves the top 3 chunks.",
        "- Config B retrieves the top 5 chunks.",
        "- Each configuration evaluates 15 questions.",
        "- Answers are checked for expected keywords, sections and citations.",
        "- Unsupported operational questions must return exactly 'I don't know'.",
        "- API errors are excluded from the answer-quality pass-rate denominator.",
        "- A final winner is selected only when both configurations complete without API errors.",
        "",
        "## Limitations",
        "",
        "- Keyword matching is an approximate evaluation method.",
        "- A passing score does not guarantee legal correctness.",
        "- API retries and delays can affect response-time measurements.",
        "- Retrieved citations still require verification against the legal PDFs.",
        "- Only top-k was varied; chunk size was kept constant.",
    ])

    REPORT_FILE.write_text(
        "\n".join(report) + "\n",
        encoding="utf-8",
    )

    print("\nEvaluation complete!")
    print("\nConfiguration comparison:")

    for row in summary:
        print(
            f"{row['configuration']}: "
            f"{row['passed']}/{row['valid_questions']} passed "
            f"({row['pass_rate']}%), "
            f"API errors: {row['api_errors']}, "
            f"avg {row['average_time_seconds']}s"
        )

    print(f"\nWinner: {winner_text}")
    print(f"Results: {RESULTS_FILE}")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    run_evaluation()
