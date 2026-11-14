
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from app.records import get_by_id, load_records
from app.smart_search import smart_search

from app.chat_service import generate_chat_answer

app = FastAPI(
    title="ChalanCheck API",
    description="API for explaining Indian traffic challan records.",
    version="1.0.0",
)


class QuestionRequest(BaseModel):
    question: str = Field(min_length=1)

class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    prompt_version: str = Field(default="v2", pattern="^(v1|v2)$")


class ChatResponse(BaseModel):
    answer: str
    confidence: str
    follow_up: str


@app.get("/health")
def health():
    """Check whether the API is running."""
    return {"status": "ok"}


@app.get("/records")
def list_records(limit: int = Query(default=10, ge=1)):
    """Return a limited number of traffic records."""
    records = load_records()
    return {
        "total": len(records),
        "records": records[:limit],
    }


@app.get("/records/{id}")
def get_record(id: str):
    """Retrieve a traffic record by its section number."""
    record = get_by_id(id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail=f"Record with section {id} not found",
        )

    return record


@app.get("/search")
def search_records(q: str = Query(min_length=1)):
    """Search and rank traffic records using TF-IDF."""
    results = smart_search(q)

    return {
        "query": q,
        "count": len(results),
        "results": results,
    }

@app.post("/questions")
def submit_question(request: QuestionRequest) -> dict[str, Any]:
    """Accept a question for future question-answering integration."""
    return {
        "question": request.question,
        "status": "received",
        "message": "Question received. Answer generation is not implemented yet.",
    }

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Explain a traffic challan question using legal records and Gemini."""
    try:
        return generate_chat_answer(
            question=request.question,
            prompt_version=request.prompt_version,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Chat service is temporarily unavailable.",
        ) from exc