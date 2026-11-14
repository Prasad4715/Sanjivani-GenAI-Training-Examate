
"""Compare ChalanCheck task prompts using 10 evaluation questions."""

import json
from datetime import datetime, timezone
from pathlib import Path

from app.chat_service import generate_chat_answer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "eval" / "prompt_results.json"

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


def main():
    results = []

    for number, question in enumerate(QUESTIONS, start=1):
        print(f"\nTesting question {number}/10", flush=True)

        entry = {
            "number": number,
            "question": question,
            "responses": {},
        }

        for version in ("v1", "v2"):
            print(f"  Running {version}...", flush=True)

            try:
                response = generate_chat_answer(question, version)
                entry["responses"][version] = response
                print(f"  {version}: completed", flush=True)

            except Exception as exc:
                entry["responses"][version] = {
                    "error": f"{type(exc).__name__}: {exc}"
                }
                print(f"  {version}: failed", flush=True)

        results.append(entry)

        # Save progress after each question.
        OUTPUT_FILE.write_text(
            json.dumps(
                {
                    "evaluated_at": datetime.now(timezone.utc).isoformat(),
                    "model_provider": "Gemini",
                    "results": results,
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )

    print(f"\nEvaluation completed. Results saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
