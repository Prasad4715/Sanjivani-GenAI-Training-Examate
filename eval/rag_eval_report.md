# Day 8 — RAG Evaluation Results

## Configuration Comparison

Chunk size: 1200 characters

Chunk overlap: 250 characters

| Configuration | Top-k | Passed | API Errors | Pass Rate | Avg Time |
|---|---:|---:|---:|---:|---:|
| A_top3 | 3 | 15/15 | 0 | 100.0% | 9.34s |
| B_top5 | 5 | 15/15 | 0 | 100.0% | 5.05s |

**Winner:** B_top5

## Evaluation Method

- Both configurations use the same PDF chunks.
- Config A retrieves the top 3 chunks.
- Config B retrieves the top 5 chunks.
- Each configuration evaluates 15 questions.
- Answers are checked for expected keywords, sections and citations.
- Unsupported operational questions must return exactly 'I don't know'.
- API errors are excluded from the answer-quality pass-rate denominator.
- A final winner is selected only when both configurations complete without API errors.

## Limitations

- Keyword matching is an approximate evaluation method.
- A passing score does not guarantee legal correctness.
- API retries and delays can affect response-time measurements.
- Retrieved citations still require verification against the legal PDFs.
- Only top-k was varied; chunk size was kept constant.
