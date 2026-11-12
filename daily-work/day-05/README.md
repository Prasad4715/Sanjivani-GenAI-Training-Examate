# Day 5 — Understanding LLMs and Checkpoint 1

## Project
ChalanCheck — Traffic Challan Assistant

## Objective
Understand how Large Language Models work, prepare realistic questions for ChalanCheck, and demonstrate the working FastAPI application.

## Assigned Tasks

### S1 — Understanding LLMs
- Explain how Large Language Models work in simple words.
- Include one diagram showing the LLM workflow.
- Document how LLMs can help explain traffic challans.
- Prepare 10 realistic ChalanCheck user questions.
- Include the six questions specified in the project assignment.

### S2 — Checkpoint 1
- Run the FastAPI application.
- Open and demonstrate the Swagger API documentation at `/docs`.
- Explain the working of one Python function.
- Create and push the Git tag `checkpoint-1`.

## Implementation Files

| File | Purpose |
|---|---|
| `../../docs/how_llms_work.md` | LLM explanation, diagram, and 10 user questions |
| `../../app/main.py` | FastAPI application for demonstration |
| `../../app/smart_search.py` | TF-IDF search function for demonstration |
| `../../README.md` | Main project documentation |

## How to Run FastAPI

From the project root:

```powershell
python -m uvicorn app.main:app --reload
```

Open:

http://127.0.0.1:8000/docs

## Checkpoint 1 Verification

- [ ] Complete `docs/how_llms_work.md`.
- [ ] Verify the LLM diagram and 10 user questions.
- [ ] Start FastAPI successfully.
- [ ] Demonstrate the API through Swagger UI.
- [ ] Explain one Python function.
- [ ] Commit and push Day 1–5 documentation.
- [ ] Create and push the `checkpoint-1` Git tag.

## One-Function Explanation — FastAPI Health Check

**Function:** Health Check  
**File:** `app/main.py`  
**Endpoint:** `GET /health`

The health check function is used to verify whether the ChalanCheck backend is running properly.

When a user sends a GET request to `/health`, FastAPI executes the corresponding Python function and returns a JSON response.

**Expected response:**

```json
{
  "status": "ok"
}
```

I tested this endpoint using FastAPI Swagger UI at `http://127.0.0.1:8000/docs`.

**Test Result:**
- HTTP Status Code: 200 OK
- Response: `{"status": "ok"}`
- Result: Passed

This confirms that the ChalanCheck API is running and responding successfully.