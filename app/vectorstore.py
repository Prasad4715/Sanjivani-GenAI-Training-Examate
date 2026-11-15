
"""Persistent ChromaDB vector store for ChalanCheck."""

import re
from pathlib import Path

import chromadb

from app.chunking import chunk_all_documents
from app.embed import embed_texts, embed_query


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CHROMA_DIR = PROJECT_ROOT / "data" / "chroma"
COLLECTION_NAME = "chalancheck_legal_chunks"

ACT_SOURCE = "motor_vehicles_act_1988.pdf"
AMENDMENT_SOURCE = "motor_vehicles_amendment_act_2019.pdf"


def get_collection():
    """Open or create the persistent legal document collection."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def index_documents(batch_size: int = 32) -> int:
    """Rebuild the collection and index all legal PDF chunks."""
    if batch_size < 1:
        raise ValueError("Batch size must be positive.")

    chunks = chunk_all_documents()

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))

    existing_names = [
        collection.name for collection in client.list_collections()
    ]

    if COLLECTION_NAME in existing_names:
        client.delete_collection(COLLECTION_NAME)
        print("Removed old ChromaDB collection.")

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    print(f"\nIndexing {len(chunks)} chunks into ChromaDB...")

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]

        vectors = embed_texts(
            [chunk["text"] for chunk in batch]
        )

        collection.upsert(
            ids=[chunk["id"] for chunk in batch],
            documents=[chunk["text"] for chunk in batch],
            embeddings=vectors.tolist(),
            metadatas=[
                {
                    "source": chunk["source"],
                    "page": chunk["page"],
                    "title": chunk["title"],
                }
                for chunk in batch
            ],
        )

        processed = min(start + batch_size, len(chunks))
        print(
            f"Indexed {processed}/{len(chunks)} chunks",
            flush=True,
        )

    return collection.count()


def extract_sections(question: str) -> list[str]:
    """Extract one or more explicitly mentioned legal section numbers."""

    section_pattern = (
        r"\b(?:sections?|sec\.?)\s*"
        r"(\d+[A-Za-z]?"
        r"(?:\s*(?:,|and|&)\s*\d+[A-Za-z]?)*"
        r"(?:\s*,?\s*and\s+\d+[A-Za-z]?)?)"
    )

    sections = []

    for match in re.finditer(
        section_pattern,
        question,
        flags=re.IGNORECASE,
    ):
        numbers = re.findall(
            r"\d+[A-Za-z]?",
            match.group(1),
        )

        sections.extend(numbers)

    return list(dict.fromkeys(
        section.upper() for section in sections
    ))


def source_priority(match: dict) -> int:
    """Prioritize the Motor Vehicles Act for penalty-section queries."""
    source = match["source"].lower()

    if source == ACT_SOURCE:
        return 0

    if source == AMENDMENT_SOURCE:
        return 1

    return 2


def find_section_heading(text: str, section: str):
    """Find a legal section heading inside a document chunk."""
    return re.search(
        rf"\b{re.escape(section)}\.\s*",
        text,
        flags=re.IGNORECASE,
    )


def section_match_priority(match: dict, section: str) -> tuple:
    """Rank actual legal provisions ahead of contents-page references."""
    text = match["text"]
    heading = find_section_heading(text, section)

    if heading is None:
        return (3, 3, 3, float("inf"))

    following_text = text[heading.end():]

    # Actual legal provisions usually contain substantive legal language.
    # Contents-page entries generally contain only section titles.
    provision_indicators = (
        "whoever",
        "shall be",
        "shall",
        "punishable",
        "liable",
    )

    # Examine the text before the next section heading, if present.
    next_heading = re.search(
        r"\b\d{1,3}[A-Za-z]?\.\s+[A-Za-z]",
        following_text,
    )

    provision_text = (
        following_text[:next_heading.start()]
        if next_heading
        else following_text
    )

    is_provision = any(
        indicator in provision_text.lower()
        for indicator in provision_indicators
    )

    distance = match["distance"]

    return (
        source_priority(match),
        0 if is_provision else 1,
        0 if len(provision_text) > 100 else 1,
        distance if distance is not None else float("inf"),
    )


def semantic_search(question: str, limit: int = 5) -> list[dict]:
    """Retrieve semantic matches and prioritize requested legal sections."""

    if not question.strip():
        raise ValueError("Search question cannot be empty.")

    if limit < 1:
        raise ValueError("Search limit must be positive.")

    collection = get_collection()
    total = collection.count()

    if total == 0:
        raise RuntimeError(
            "ChromaDB collection is empty. "
            "Run python -m app.vectorstore first."
        )

    query_vector = embed_query(question)

    results = collection.query(
        query_embeddings=[query_vector.tolist()],
        n_results=min(max(limit * 10, 50), total),
        include=["documents", "metadatas", "distances"],
    )

    matches = []

    for chunk_id, document, metadata, distance in zip(
        results["ids"][0],
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        matches.append({
            "id": chunk_id,
            "text": document,
            "source": metadata["source"],
            "page": metadata["page"],
            "title": metadata["title"],
            "distance": float(distance),
        })

    requested_sections = extract_sections(question)

    # For natural-language questions without section numbers,
    # return the normal semantic results.
    if not requested_sections:
        return matches[:limit]

    # Include exact-section candidates that may not appear
    # among the semantic search results.
    all_chunks = collection.get(
        include=["documents", "metadatas"]
    )

    existing_ids = {
        match["id"] for match in matches
    }

    for chunk_id, document, metadata in zip(
        all_chunks["ids"],
        all_chunks["documents"],
        all_chunks["metadatas"],
    ):
        if chunk_id in existing_ids:
            continue

        if any(
            find_section_heading(document, section)
            for section in requested_sections
        ):
            matches.append({
                "id": chunk_id,
                "text": document,
                "source": metadata["source"],
                "page": metadata["page"],
                "title": metadata["title"],
                "distance": None,
            })

            existing_ids.add(chunk_id)

    selected = []
    selected_ids = set()

    # First, select the best available passage for each
    # explicitly requested section.
    for section in requested_sections:
        candidates = [
            match
            for match in matches
            if find_section_heading(match["text"], section)
            and match["id"] not in selected_ids
        ]

        candidates.sort(
            key=lambda match: section_match_priority(
                match,
                section,
            )
        )

        if candidates:
            best = candidates[0]
            selected.append(best)
            selected_ids.add(best["id"])

        if len(selected) >= limit:
            return selected[:limit]

    # Fill remaining positions with relevant candidates,
    # preferring actual provisions over contents-page entries.
    def remaining_priority(match):
        section_scores = [
            section_match_priority(match, section)
            for section in requested_sections
            if find_section_heading(match["text"], section)
        ]

        if section_scores:
            return (0, min(section_scores))

        distance = match["distance"]

        return (
            1,
            (
                source_priority(match),
                2,
                2,
                distance if distance is not None else float("inf"),
            ),
        )

    matches.sort(key=remaining_priority)

    for match in matches:
        if len(selected) >= limit:
            break

        if match["id"] not in selected_ids:
            selected.append(match)
            selected_ids.add(match["id"])

    return selected[:limit]


if __name__ == "__main__":
    total = index_documents()

    print(
        f"\nPersistent ChromaDB collection contains "
        f"{total} chunks."
    )
