
"""Basic API tests for ChalanCheck."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Health endpoint should confirm API availability."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_records_endpoint():
    """Records endpoint should return legal records."""
    response = client.get("/records")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "records" in data
    assert isinstance(data["records"], list)
    assert data["total"] >= 20


def test_records_limit():
    """Records endpoint should respect the limit parameter."""
    response = client.get("/records?limit=2")

    assert response.status_code == 200

    data = response.json()

    assert len(data["records"]) == 2
    assert data["total"] >= 2



def test_get_existing_record():
    """A valid section should return its legal record."""
    response = client.get("/records/194D")

    assert response.status_code == 200

    data = response.json()

    assert str(data["section"]).upper() == "194D"


def test_get_nonexistent_record():
    """An unknown section should return HTTP 404."""
    response = client.get("/records/999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()



def test_search_endpoint(monkeypatch):
    """Search should return matching legal records."""

    def fake_search(query):
        return [
            {
                "section": "185",
                "offence": "Driving under the influence of alcohol",
            }
        ]

    monkeypatch.setattr("app.main.smart_search", fake_search)

    response = client.get("/search?q=drunk driving")

    assert response.status_code == 200

    data = response.json()

    assert data["query"] == "drunk driving"
    assert data["count"] == 1
    assert data["results"][0]["section"] == "185"


def test_search_empty_query():
    """An empty search query should be rejected."""
    response = client.get("/search?q=")

    assert response.status_code == 422


def test_ask_endpoint_with_fake_llm(monkeypatch):
    """Test RAG API without calling a real LLM."""

    def fake_ask_question(question, top_k):
        return {
            "question": question,
            "answer": "Section 185 covers drunk driving.",
            "citations": [],
            "retrieved_chunks": 1,
        }

    monkeypatch.setattr(
        "app.main.ask_question",
        fake_ask_question
    )

    response = client.post(
        "/ask",
        json={
            "question": "What is Section 185?",
            "top_k": 3
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["question"] == "What is Section 185?"
    assert data["answer"] == "Section 185 covers drunk driving."
    assert data["retrieved_chunks"] == 1
    assert data["citations"] == []


def test_agent_fine_calculator():
    """Verify that the agent tool calculates fines correctly."""

    from app.tools import challan_total_calculator

    result = challan_total_calculator(
        sections=["180", "181"],
        repeat_offence=False
    )

    assert result["total_maximum_fine"] == 10000
    assert result["known_fines_subtotal"] == 10000
    assert result["currency"] == "INR"
    assert result["complete"] is True
    assert result["unknown_sections"] == []
    assert result["missing_fine_sections"] == []
    assert len(result["fine_breakdown"]) == 2
