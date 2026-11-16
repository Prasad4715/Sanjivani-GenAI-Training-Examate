"""Persistent ChromaDB vector store and section-aware retrieval for ChalanCheck."""

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
    """Rebuild the collection using PDF chunks with ordering metadata."""
    if batch_size < 1:
        raise ValueError("Batch size must be positive.")

    chunks = chunk_all_documents()
    if not chunks:
        raise ValueError("No document chunks were generated.")
    if any("chunk_index" not in chunk for chunk in chunks):
        raise ValueError("Update app/chunking.py to provide chunk_index first.")

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    if COLLECTION_NAME in [c.name for c in client.list_collections()]:
        client.delete_collection(COLLECTION_NAME)
        print("Removed old ChromaDB collection.")

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    print(f"\nIndexing {len(chunks)} chunks into ChromaDB...")

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        vectors = embed_texts([chunk["text"] for chunk in batch])
        collection.upsert(
            ids=[chunk["id"] for chunk in batch],
            documents=[chunk["text"] for chunk in batch],
            embeddings=vectors.tolist(),
            metadatas=[
                {
                    "source": chunk["source"],
                    "page": chunk["page"],
                    "chunk_index": chunk["chunk_index"],
                    "title": chunk["title"],
                }
                for chunk in batch
            ],
        )
        print(f"Indexed {min(start + batch_size, len(chunks))}/{len(chunks)} chunks", flush=True)

    return collection.count()


def extract_sections(question: str) -> list[str]:
    """Read explicit section references, including 206(4) and 194D/196."""
    pattern = (
        r"\b(?:sections?|sec\.?)\s*"
        r"(\d+[A-Za-z]?(?:\s*\(\d+\))?"
        r"(?:\s*(?:,|/|&|and)\s*\d+[A-Za-z]?(?:\s*\(\d+\))?)*)"
    )
    sections = []
    for match in re.finditer(pattern, question, flags=re.IGNORECASE):
        sections.extend(re.findall(r"\d+[A-Za-z]?", re.sub(r"\(\d+\)", "", match.group(1))))
    return list(dict.fromkeys(section.upper() for section in sections))


def infer_sections(question: str) -> list[str]:
    """Infer Section 206 only for clearly worded licence-impoundment queries."""
    lower = question.lower()
    mentions_licence = bool(re.search(r"\b(?:driving\s+)?licen[cs]e\b", lower))
    mentions_impound = bool(re.search(r"\bimpound(?:ed|ing|ment)?\b", lower))
    if mentions_licence and mentions_impound:
        return ["206"]
    return []


def source_priority(match: dict) -> int:
    """Prefer the principal Act, then its 2019 amendment."""
    source = match["source"].lower()
    if source == ACT_SOURCE:
        return 0
    if source == AMENDMENT_SOURCE:
        return 1
    return 2


def find_section_heading(text: str, section: str):
    """Find a numbered section heading (not a mere mention of a section)."""
    return re.search(
        rf"(?<!\w){re.escape(section)}\.\s+[A-Za-z]",
        text,
        flags=re.IGNORECASE,
    )


def section_match_priority(match: dict, section: str) -> tuple:
    """Rank actual section text ahead of index/table-of-contents references."""
    heading = find_section_heading(match["text"], section)
    if heading is None:
        return (3, 3, 3, float("inf"))

    following = match["text"][heading.end():]
    next_heading = re.search(r"\b\d{1,3}[A-Za-z]?\.\s+[A-Za-z]", following)
    provision = following[:next_heading.start()] if next_heading else following
    indicators = ("whoever", "shall", "punishable", "liable", "police officer", "may, if")
    substantive = any(word in provision.lower() for word in indicators)
    distance = match.get("distance")
    return (
        0 if substantive else 1,
        source_priority(match),
        0 if len(provision) > 100 else 1,
        distance if distance is not None else float("inf"),
    )


def _as_match(chunk_id: str, document: str, metadata: dict, distance=None) -> dict:
    """Convert ChromaDB fields to the search-result format."""
    if "chunk_index" not in metadata:
        raise RuntimeError(
            "ChromaDB has old metadata without chunk_index. "
            "Run python -m app.vectorstore to rebuild the index."
        )
    return {
        "id": chunk_id,
        "text": document,
        "source": metadata["source"],
        "page": metadata["page"],
        "chunk_index": metadata["chunk_index"],
        "title": metadata["title"],
        "distance": float(distance) if distance is not None else None,
    }



def expand_adjacent_chunks(matches: list[dict], limit: int) -> list[dict]:
    """Expand selected results with consecutive chunks from the same PDF."""
    collection = get_collection()
    data = collection.get(include=["documents", "metadatas"])

    by_source = {}

    for chunk_id, document, metadata in zip(
        data["ids"], data["documents"], data["metadatas"]
    ):
        source = metadata["source"]

        by_source.setdefault(source, []).append({
            "id": chunk_id,
            "text": document,
            "source": source,
            "page": metadata["page"],
            "chunk_index": metadata.get("chunk_index", 0),
            "title": metadata["title"],
            "distance": None,
        })

    positions = {}

    for source, chunks in by_source.items():
        chunks.sort(key=lambda c: (c["page"], c["chunk_index"]))

        for position, chunk in enumerate(chunks):
            positions[chunk["id"]] = (source, position)

    expanded = []
    seen = set()

    for match in matches:
        if len(expanded) >= limit:
            break

        location = positions.get(match["id"])
        if location is None:
            continue

        source, position = location
        document_chunks = by_source[source]

        # Include the matched chunk and consecutive following chunks.
        for chunk in document_chunks[position:position + limit]:
            if len(expanded) >= limit:
                break

            if chunk["id"] in seen:
                continue

            expanded.append(
                match if chunk["id"] == match["id"] else chunk
            )
            seen.add(chunk["id"])

    return expanded

def semantic_search(question: str, limit: int = 5) -> list[dict]:
    """Search legal passages, prioritizing sections and their continuations."""
    if not question.strip():
        raise ValueError("Search question cannot be empty.")
    if limit < 1:
        raise ValueError("Search limit must be positive.")

    collection = get_collection()
    total = collection.count()
    if total == 0:
        raise RuntimeError(
            "ChromaDB collection is empty. Run python -m app.vectorstore first."
        )

    query_vector = embed_query(question)
    results = collection.query(
        query_embeddings=[query_vector.tolist()],
        n_results=min(max(limit * 10, 50), total),
        include=["documents", "metadatas", "distances"],
    )
    matches = [
        _as_match(chunk_id, document, metadata, distance)
        for chunk_id, document, metadata, distance in zip(
            results["ids"][0],
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]

    sections = extract_sections(question)
    if not sections:
        sections = infer_sections(question)

    # Preserve ordinary semantic search when no section can be identified.
    if not sections:
        return matches[:limit]

    # Find section headings even when vector similarity did not rank them highly.
    all_chunks = collection.get(include=["documents", "metadatas"])
    known_ids = {match["id"] for match in matches}
    for chunk_id, document, metadata in zip(
        all_chunks["ids"], all_chunks["documents"], all_chunks["metadatas"]
    ):
        if chunk_id not in known_ids and any(
            find_section_heading(document, section) for section in sections
        ):
            matches.append(_as_match(chunk_id, document, metadata))
            known_ids.add(chunk_id)

    # Reserve slots for neighboring chunks, but keep all requested sections.
    primary_limit = min(limit, max(len(sections), (limit + 1) // 2))
    selected = []
    selected_ids = set()

    for section in sections:
        candidates = [
            match for match in matches
            if match["id"] not in selected_ids
            and find_section_heading(match["text"], section)
        ]
        candidates.sort(key=lambda match: section_match_priority(match, section))
        if candidates:
            best = candidates[0]
            selected.append(best)
            selected_ids.add(best["id"])
        if len(selected) >= primary_limit:
            return expand_adjacent_chunks(selected, limit)

    # Prefer other matching sections, then fill with semantic results.
    def remaining_priority(match: dict):
        scores = [
            section_match_priority(match, section)
            for section in sections
            if find_section_heading(match["text"], section)
        ]
        if scores:
            return (0, min(scores))
        distance = match.get("distance")
        return (1, distance if distance is not None else float("inf"))

    for match in sorted(matches, key=remaining_priority):
        if len(selected) >= primary_limit:
            break
        if match["id"] not in selected_ids:
            selected.append(match)
            selected_ids.add(match["id"])

    return expand_adjacent_chunks(selected, limit)


if __name__ == "__main__":
    total = index_documents()
    print(f"\nPersistent ChromaDB collection contains {total} chunks.")
