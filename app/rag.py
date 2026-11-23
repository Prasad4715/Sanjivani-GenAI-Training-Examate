
"""Retrieval-Augmented Generation for ChalanCheck."""

import re

from app.cache import get_cached_answer, set_cached_answer
from app.llm import LLMProvider
from app.vectorstore import semantic_search

RAG_SYSTEM_PROMPT = """
You are ChalanCheck, an Indian traffic challan explanation assistant.

Answer questions using ONLY the retrieved legal document passages.

Rules:
1. Explain the legal information in simple English.
2. Mention the relevant Motor Vehicles Act section.
3. Explain the offence, penalty and additional action only when supported.
4. Do not invent legal provisions, fines or punishments.
5. Distinguish statutory penalties from actual challan amounts.
6. If the passages do not contain enough information to answer,
   respond exactly: I don't know
7. Do not guess police station opening hours, Sunday availability,
   local payment facilities or other operational information.
8. Cite evidence using the supplied source labels, such as [1] or [2].
9. If multiple sections are requested, explain each separately.
10. Do not use outside knowledge to fill gaps in the passages.
"""


def is_operational_question(question: str) -> bool:
    """Detect questions requiring live local service information."""
    text = question.lower()

    operational_terms = (
        "open on sunday",
        "on sunday",
        "opening hours",
        "closing time",
        "police station open",
        "pay at police station",
        "payment counter",
        "office hours",
    )

    return any(term in text for term in operational_terms)


def build_context(chunks: list[dict]) -> str:
    """Format retrieved chunks with numbered source citations."""
    passages = []

    for number, chunk in enumerate(chunks, start=1):
        source = chunk["source"]
        page = chunk["page"]
        title = chunk["title"]
        text = chunk["text"]

        passages.append(
            f"[{number}]\n"
            f"Document: {source}\n"
            f"Title: {title}\n"
            f"Page: {page}\n"
            f"Legal text:\n{text}"
        )

    return "\n\n".join(passages)


def ask_question(
    question: str,
    top_k: int = 5,
    llm: LLMProvider | None = None,
) -> dict:
    """Answer a question using retrieved legal evidence."""

    # Validate question
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    # Validate retrieval limit
    if top_k < 1 or top_k > 20:
        raise ValueError("top_k must be between 1 and 20.")

    # Normalize the question for caching
    normalized_question = question.strip()

    # Include retrieval limit in cache key
    cache_key = (normalized_question, top_k)

    # Disable cache when a custom LLM is supplied
    use_cache = llm is None

    # Step 1: Check cache
    if use_cache:
        cached_result = get_cached_answer(cache_key)

        if cached_result is not None:
            return cached_result

    # Step 2: Handle unsupported operational questions
    if is_operational_question(question):
        return {
            "question": question,
            "answer": "I don't know",
            "citations": [],
            "retrieved_chunks": 0,
        }

    # Step 3: Retrieve legal evidence
    chunks = semantic_search(
        question,
        limit=top_k,
    )

    if not chunks:
        return {
            "question": question,
            "answer": "I don't know",
            "citations": [],
            "retrieved_chunks": 0,
        }

    # Step 4: Build evidence context
    context = build_context(chunks)

    prompt = f"""
Use the following legal evidence to answer the user's question.

RETRIEVED LEGAL PASSAGES:
{context}

USER QUESTION:
{question}

INSTRUCTIONS:
- Answer only if the evidence supports the answer.
- Cite the relevant passage numbers in square brackets.
- If evidence is insufficient, say exactly: I don't know
"""

    # Step 5: Generate answer using Gemini
    provider = llm if llm is not None else LLMProvider()

    answer = provider.generate(
        question=prompt,
        system_prompt=RAG_SYSTEM_PROMPT,
    ).strip()

    # Step 6: Handle insufficient evidence
    if not answer or answer.lower().startswith("i don't know"):
        return {
            "question": question,
            "answer": "I don't know",
            "citations": [],
            "retrieved_chunks": len(chunks),
        }

    # Step 7: Extract legal citations
    # Supports [1], [2], and grouped citations such as [1, 3]
    cited_numbers = set()

    for citation_group in re.findall(
        r"\[([0-9,\s]+)\]",
        answer,
    ):
        for number in re.findall(r"\d+", citation_group):
            reference = int(number)

            if 1 <= reference <= len(chunks):
                cited_numbers.add(reference)

    # Step 8: Reject answers without valid citations
    if not cited_numbers:
        return {
            "question": question,
            "answer": "I don't know",
            "citations": [],
            "retrieved_chunks": len(chunks),
        }

    # Step 9: Prepare citation details
    citations = [
        {
            "reference": f"[{number}]",
            "source": chunks[number - 1]["source"],
            "page": chunks[number - 1]["page"],
            "title": chunks[number - 1]["title"],
        }
        for number in sorted(cited_numbers)
    ]

    # Step 10: Prepare final response
    result = {
        "question": question,
        "answer": answer,
        "citations": citations,
        "retrieved_chunks": len(chunks),
    }

    # Step 11: Cache only successful, cited answers
    if use_cache:
        set_cached_answer(cache_key, result)

    return result
