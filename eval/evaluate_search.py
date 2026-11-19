
"""Evaluate ChalanCheck semantic search using ten questions."""

from pathlib import Path

from app.vectorstore import semantic_search

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "eval" / "search_results.md"

QUESTIONS = [
    "What is the fine for riding bike without helmet under section 194D?",
    "What is section 196 in my challan, driving without insurance?",
    "Under which section can the police seize my driving licence on the spot?",
    "I got challan for no helmet and no insurance together, what is the total maximum fine?",
    "My son is 16 and drove the scooty, what penalty for him and for me as the owner?",
    "Can I pay my Maharashtra e-challan at Kopargaon police station on Sunday?",
    "I received a challan under Section 183 for speeding. What is the maximum fine?",
    "What happens if I am caught drunk driving for the second time under Section 185?",
    "My challan mentions Section 184. What does dangerous driving mean, and what additional punishment can apply?",
    "I received a challan with Sections 194D and 196. Can ChalanCheck explain both violations separately?",
]


def evaluate():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Day 7 — Semantic Search Evaluation",
        "",
        "Search method: ChromaDB cosine similarity with section-aware reranking.",
        "",
        "These are retrieved passages, not verified legal answers.",
        "Lower distance means greater semantic similarity.",
        "A missing distance indicates an exact-section candidate added during reranking.",
        "",
    ]

    for number, question in enumerate(QUESTIONS, start=1):
        print(f"Evaluating question {number}/10...", flush=True)

        lines.extend([
            f"## Question {number}",
            "",
            f"**Question:** {question}",
            "",
        ])

        try:
            results = semantic_search(question, limit=3)

            for rank, result in enumerate(results, start=1):
                distance = result["distance"]
                distance_text = (
                    f"{distance:.4f}" if distance is not None else "Not calculated"
                )

                lines.extend([
                    f"### Result {rank}",
                    "",
                    f"- Source: `{result['source']}`",
                    f"- PDF page: {result['page']}",
                    f"- Title: {result['title']}",
                    f"- Distance: {distance_text}",
                    "",
                    "**Retrieved passage:**",
                    "",
                    f"> {result['text'][:800]}",
                    "",
                ])

        except Exception as error:
            lines.extend([
                f"**Search error:** {type(error).__name__}: {error}",
                "",
            ])

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")

    print(f"\nEvaluation saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    evaluate()
