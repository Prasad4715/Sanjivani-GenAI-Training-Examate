# Day 8 — RAG Integration, Retrieval Improvements and Evaluation

## Project: ChalanCheck

### Objective
Implement Retrieval-Augmented Generation (RAG) using Gemini and ChromaDB to answer traffic challan questions with explanations grounded in official Motor Vehicles Act and Rules PDFs.

## S1 — RAG Pipeline and Gemini Integration

Created `app/rag.py` to connect semantic retrieval with Gemini-based answer generation.

- Retrieved relevant legal document chunks from ChromaDB.
- Used Gemini to generate answers based on retrieved legal text.
- Included source citations with document names and page numbers.
- Implemented question answering using the `ask_question()` function.
- Used configurable `top_k` retrieval to control the number of document chunks.

## S2 — Retrieval Improvements and RAG Evaluation

Updated `app/chunking.py` and `app/vectorstore.py` to improve legal section retrieval.

- Added `chunk_index` metadata to preserve chunk ordering.
- Improved section-aware retrieval for specific Motor Vehicles Act sections.
- Added adjacent-chunk retrieval for legal provisions spanning multiple chunks or pages.
- Improved retrieval for questions mentioning multiple sections.
- Preserved relevant context for Sections 185, 192A, 194D, 196 and 206(4).
- Reduced the risk of one section occupying all available retrieval slots.

Created the following evaluation files:

- `eval/eval_set.json` — Contains 15 traffic challan evaluation questions.
- `eval/run_eval.py` — Evaluates RAG responses using different retrieval configurations.
- `eval/rag_eval_results.json` — Stores detailed evaluation results locally.
- `eval/rag_eval_report.md` — Contains the evaluation summary.

## FastAPI Integration

Updated `app/main.py` to integrate RAG-based question answering.

Added the endpoint:

`POST /ask`

The endpoint accepts a traffic challan question and a configurable `top_k` value.

It returns:

- User question
- Generated answer
- Source citations
- Number of retrieved chunks

Set the default retrieval configuration to `top_k=5`.

## Evaluation

Evaluated the RAG pipeline using 15 traffic challan questions.

Compared two retrieval configurations:

| Configuration | Passed | Pass Rate | Average Response Time |
|---|---|---|---|
| A_top3 | 15/15 | 100% | 9.34 seconds |
| B_top5 | 15/15 | 100% | 5.05 seconds |

Selected **B_top5** as the preferred configuration.

Verified successful keyword checks for:

- Helmet violations under Section 194D.
- Driving without insurance under Section 196.
- Driving without a valid licence under Section 181.
- Repeat drunk-driving offences under Section 185.
- Dangerous driving under Section 184.
- Multi-section questions involving Sections 194D and 196.
- Licence impoundment under Section 206(4).
- Driving without a permit under Section 192A.

Final evaluation result: **15/15 keyword checks passed for both configurations.**

## Challenges and Improvements

- Initial evaluation achieved 14/15 keyword checks.
- Some retrieved results contained irrelevant table-of-contents entries.
- Adjacent-chunk retrieval initially prioritized consecutive chunks from one section.
- Improved retrieval to preserve multiple requested sections.
- Re-evaluated the system and achieved 15/15 keyword checks.
- Handled temporary Gemini API errors using retry logic in the evaluation process.

## Limitations

- A 100% keyword evaluation pass rate does not guarantee complete legal accuracy.
- Some retrieved chunks may still contain unrelated legal text.
- Gemini API availability and response times may vary.
- Questions about local police station services cannot be verified using legal PDFs alone.
- Legal penalties and additional consequences must be verified against applicable official sources.

## Dependencies

- chromadb
- sentence-transformers
- pymupdf
- FastAPI
- Gemini API integration

## Commands

Check Python dependencies:

    python -m pip check

Rebuild the vector database when source documents or chunk metadata change:

    python -m app.vectorstore

Run RAG evaluation:

    python -u -m eval.run_eval

Start FastAPI:

    python -m uvicorn app.main:app --reload

API documentation:

    http://127.0.0.1:8000/docs

RAG endpoint:

    POST /ask

## Outcome

Completed Gemini-based RAG integration, improved section-aware retrieval, adjacent-chunk expansion, multi-section retrieval, source citations, FastAPI question-answering integration and automated RAG evaluation.

Achieved **15/15 keyword evaluation checks (100%)** for both Top 3 and Top 5 retrieval configurations.

Selected Top 5 retrieval as the default configuration for ChalanCheck.