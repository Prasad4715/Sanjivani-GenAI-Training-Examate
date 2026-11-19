
"""FastAPI application for ChalanCheck."""

from typing import Any

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, model_validator

from app.chat_service import generate_chat_answer
from app.graph import graph, run_graph
from app.rag import ask_question
from app.records import get_by_id, load_records
from app.smart_search import smart_search
from app.vectorstore import semantic_search

app = FastAPI(
    title="ChalanCheck API",
    description=(
        "API for explaining Indian traffic challans "
        "using legal records, semantic search, RAG, "
        "and a LangGraph agent."
    ),
    version="1.2.0",
)


# --------------------------------------------------
# Request and Response Models
# --------------------------------------------------

class QuestionRequest(BaseModel):
    question: str = Field(min_length=1)


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    prompt_version: str = Field(
        default="v2",
        pattern="^(v1|v2)$",
    )


class ChatResponse(BaseModel):
    answer: str
    confidence: str
    follow_up: str


class AskRequest(BaseModel):
    """Request model for RAG-based question answering."""

    question: str = Field(
        min_length=1,
        description="Traffic challan question",
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of legal chunks to retrieve",
    )


class CitationResponse(BaseModel):
    reference: str
    source: str
    page: int
    title: str


class AskResponse(BaseModel):
    question: str
    answer: str
    citations: list[CitationResponse]
    retrieved_chunks: int


# --------------------------------------------------
# Day 9: LangGraph Agent Models
# --------------------------------------------------

class AgentRequest(BaseModel):
    """Start a new agent question or resume an approval."""

    session_id: str = Field(
        min_length=1,
        max_length=100,
        description="Unique conversation session ID",
    )

    question: str | None = Field(
        default=None,
        description="New question for the agent",
    )

    approve: bool | None = Field(
        default=None,
        description=(
            "True to approve a pending calculation; "
            "False to reject it"
        ),
    )

    @model_validator(mode="after")
    def validate_action(self):
        """Require either a question or approval, not both."""

        has_question = (
            self.question is not None
            and bool(self.question.strip())
        )

        has_approval = self.approve is not None

        if has_question == has_approval:
            raise ValueError(
                "Provide either a non-empty question "
                "or an approval decision, not both."
            )

        return self


class AgentResponse(BaseModel):
    """Response from the LangGraph agent."""

    session_id: str
    pending_approval: bool
    approval_request: dict[str, Any] | None = None
    answer: str | None = None
    sections: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    history: list[dict[str, str]] = Field(
        default_factory=list
    )


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/health")
def health():
    """Check whether the API is running."""
    return {"status": "ok"}


# --------------------------------------------------
# Legal Records
# --------------------------------------------------

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


# --------------------------------------------------
# TF-IDF Search
# --------------------------------------------------

@app.get("/search")
def search_records(q: str = Query(min_length=1)):
    """Search and rank traffic records using TF-IDF."""

    results = smart_search(q)

    return {
        "query": q,
        "count": len(results),
        "results": results,
    }


# --------------------------------------------------
# Question Submission
# --------------------------------------------------

@app.post("/questions")
def submit_question(
    request: QuestionRequest,
) -> dict[str, Any]:
    """Accept a question for future question-answering integration."""

    return {
        "question": request.question,
        "status": "received",
        "message": (
            "Question received. "
            "Use POST /ask for RAG-based answers."
        ),
    }


# --------------------------------------------------
# Day 6: Gemini Chat
# --------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Explain traffic challans using legal records and Gemini."""

    try:
        return generate_chat_answer(
            question=request.question,
            prompt_version=request.prompt_version,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Chat service is temporarily unavailable.",
        ) from exc


# --------------------------------------------------
# Day 7: Semantic Search
# --------------------------------------------------

@app.get("/search/semantic")
def search_semantic(
    q: str,
    limit: int = 5,
):
    """Search legal PDF chunks using ChromaDB semantic retrieval."""

    if not q.strip():
        raise HTTPException(
            status_code=400,
            detail="Search question cannot be empty.",
        )

    if limit < 1 or limit > 20:
        raise HTTPException(
            status_code=400,
            detail="Limit must be between 1 and 20.",
        )

    try:
        results = semantic_search(
            question=q,
            limit=limit,
        )

        return {
            "query": q,
            "total_results": len(results),
            "results": results,
        }

    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc


# --------------------------------------------------
# Day 8: RAG Question Answering
# --------------------------------------------------

@app.post("/ask", response_model=AskResponse)
def ask_chalancheck(request: AskRequest):
    """
    Answer traffic challan questions using RAG.

    Steps:
    1. Receive the user's question.
    2. Retrieve relevant legal chunks from ChromaDB.
    3. Generate an answer using Gemini.
    4. Return the answer with PDF citations.
    5. Say "I don't know" when information is unavailable.
    """

    try:
        result = ask_question(
            question=request.question,
            top_k=request.top_k,
        )

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="Question answering is temporarily unavailable.",
        ) from exc


# --------------------------------------------------
# Day 9: LangGraph Agent
# --------------------------------------------------

@app.post("/agent", response_model=AgentResponse)
def agent_endpoint(request: AgentRequest):
    """
    Run the LangGraph agent.

    Features:
    - RAG-based legal explanations
    - Maximum fine calculations
    - Conversation memory
    - Human approval before calculation
    - Approval and rejection handling
    """

    config = {
        "configurable": {
            "thread_id": request.session_id
        }
    }

    try:
        snapshot = graph.get_state(config)

        # ------------------------------------------
        # Resume a pending approval
        # ------------------------------------------

        if request.approve is not None:

            if (
                not snapshot.next
                or "approval" not in snapshot.next
            ):
                raise HTTPException(
                    status_code=409,
                    detail=(
                        "No pending approval exists "
                        "for this session."
                    ),
                )

            result = run_graph(
                session_id=request.session_id,
                approve=request.approve,
            )

            return result

        # ------------------------------------------
        # Start a new question
        # ------------------------------------------

        if snapshot.next:
            raise HTTPException(
                status_code=409,
                detail=(
                    "This session has a pending approval. "
                    "Approve or reject the calculation "
                    "before asking another question."
                ),
            )

        result = run_graph(
            question=request.question,
            session_id=request.session_id,
        )

        return result

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Agent service is temporarily unavailable."
            ),
        ) from exc
