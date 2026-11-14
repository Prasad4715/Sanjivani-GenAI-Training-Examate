# Day 6 — LLM Integration and Prompt Engineering

## Objective

Integrate Google Gemini into ChalanCheck and develop prompts that explain Indian traffic challans in simple English using available legal records.

## S1 — LLM Provider Integration

### Tasks Completed

1. Installed `google-genai` and `python-dotenv`.
2. Created `app/llm.py` as a reusable Gemini provider wrapper.
3. Configured the Gemini model using environment variables.
4. Created `.env.example` with placeholder configuration.
5. Protected `.env` using `.gitignore`.
6. Added a POST `/chat` endpoint to the FastAPI application.
7. Connected the chat service to the existing legal-record retrieval system.
8. Implemented JSON responses containing:
   - `answer`
   - `confidence`
   - `follow_up`

### Files Created or Updated

- `app/llm.py`
- `app/chat_service.py`
- `app/main.py`
- `.env.example`
- `.gitignore`
- `requirements.txt`

## S2 — Prompt Engineering and Evaluation

### Tasks Completed

1. Created `prompts/system.txt` with ChalanCheck's role, responsibilities, and accuracy rules.
2. Created `prompts/task_v1.txt` for basic challan explanations.
3. Created `prompts/task_v2.txt` for structured, evidence-based explanations.
4. Prepared 10 evaluation questions covering traffic violations, multiple offences, and unavailable information.
5. Tested both prompt versions using Google Gemini.
6. Generated 20 successful responses after retrying two temporary API failures.
7. Compared the responses for clarity, completeness, relevance, and uncertainty handling.
8. Selected Prompt V2 as the default prompt.

### Files Created

- `prompts/system.txt`
- `prompts/task_v1.txt`
- `prompts/task_v2.txt`
- `eval/compare_prompts.py`
- `eval/prompt_results.json`
- `eval/prompt_review.md`
- `eval/prompt_compare.md`

## Testing and Verification

- Gemini API connection tested successfully.
- POST `/chat` endpoint tested successfully.
- Python dependency check completed without detected conflicts.
- Gemini model configuration verified.
- `.env` confirmed ignored and untracked by Git.
- Prompt comparison completed with 20/20 successful API responses.

## Observations

- Prompt V2 provides more consistent and structured explanations.
- Prompt V1 can be more concise for straightforward questions.
- Everyday offence descriptions sometimes fail to retrieve the correct legal records.
- Some legal provisions are missing from the current dataset.
- Legal penalty values require further verification against official sources.
- The current confidence field is a basic heuristic rather than a calibrated confidence score.

## Outcome

Completed Day 6 LLM integration and prompt engineering requirements.

ChalanCheck can now accept traffic challan questions through its FastAPI `/chat` endpoint, retrieve relevant legal records, generate explanations using Gemini, and return structured JSON responses.

Prompt V2 is selected as the default version for future development.