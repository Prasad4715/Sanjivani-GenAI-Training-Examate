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

# Section headings normally look like "194D. Penalty for ...".
# A heading can appear in the middle of a PDF chunk.
HEADING_PATTERN = re.compile(r"(?<![\w.])(?P<section>\d{1,3}[A-Za-z]?)\.\s+(?=[A-Za-z])")
SECTION_REFERENCE = re.compile(r"\b(?:sections?|sec\.)\s*", re.IGNORECASE)
SECTION_TOKEN = re.compile(r"\d{1,3}[A-Za-z]?(?:\s*\(\s*\d+\s*\))?")
JOINER = re.compile(r"\s*(?:,|/|&|\band\b|\bor\b)\s*", re.IGNORECASE)


def get_collection():
    """Open or create the persistent legal document collection."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def index_documents(batch_size: int = 32) -> int:
    """Rebuild the collection from PDF chunks with ordering metadata."""
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
        print(
            f"Indexed {min(start + batch_size, len(chunks))}/{len(chunks)} chunks",
            flush=True,
        )
    return collection.count()


def extract_sections(question: str) -> list[str]:
    """Extract explicitly named sections; keep 206(4) associated with 206."""
    sections = []
    for reference in SECTION_REFERENCE.finditer(question):
        position = reference.end()
        token = SECTION_TOKEN.match(question, position)
        if token is None:
            continue
        while token is not None:
            # Retrieve the parent section's heading, including for subsection queries.
            section = re.match(r"\d{1,3}[A-Za-z]?", token.group()).group().upper()
            if section not in sections:
                sections.append(section)
            position = token.end()
            joiner = JOINER.match(question, position)
            if joiner is None:
                break
            position = joiner.end()
            token = SECTION_TOKEN.match(question, position)
    return sections


def infer_sections(question: str) -> list[str]:
    """Infer Section 206 for explicit driving-licence impoundment questions."""
    lower = question.lower()
    mentions_licence = bool(re.search(r"\b(?:driving\s+)?licen[cs]e\b", lower))
    mentions_impound = bool(re.search(r"\bimpound(?:ed|ing|ment)?\b", lower))
    return ["206"] if mentions_licence and mentions_impound else []


def source_priority(match: dict) -> int:
    """Prefer the consolidated principal Act over the amendment and rules."""
    source = match["source"].lower()
    if source == ACT_SOURCE:
        return 0
    if source == AMENDMENT_SOURCE:
        return 1
    return 2


def find_section_heading(text: str, section: str):
    """Match a heading, not a mere cross-reference to a section."""
    section = section.upper()
    for heading in HEADING_PATTERN.finditer(text):
        if heading.group("section").upper() == section:
            return heading
    return None


def section_match_priority(match: dict, section: str) -> tuple:
    """Prefer substantive headings in the principal Act over index entries."""
    heading = find_section_heading(match["text"], section)
    if heading is None:
        return (3, 3, 3, float("inf"))

    following = match["text"][heading.end():]
    next_heading = HEADING_PATTERN.search(following)
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
    """Convert ChromaDB fields to the existing search-result format."""
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


def _ordered_chunks(all_chunks: dict) -> tuple[dict, dict]:
    """Build source-local chunk sequences and a lookup of chunk positions."""
    by_source = {}
    for chunk_id, document, metadata in zip(
        all_chunks["ids"], all_chunks["documents"], all_chunks["metadatas"]
    ):
        match = _as_match(chunk_id, document, metadata)
        by_source.setdefault(match["source"], []).append(match)

    positions = {}
    for source, chunks in by_source.items():
        chunks.sort(key=lambda chunk: (int(chunk["page"]), int(chunk["chunk_index"])))
        for position, chunk in enumerate(chunks):
            positions[chunk["id"]] = (source, position)
    return by_source, positions


def _continuation_chunks(seed: dict, by_source: dict, positions: dict):
    """Yield later chunks until the next distinct section heading.

    A provision can cross PDF pages, so continuation is based on source-local
    chunk order, not on page equality.
    """
    location = positions.get(seed["id"])
    if location is None:
        return
    source, position = location
    chunks = by_source[source]
    # Do not pull arbitrary pages into the answer. Three continuations is a
    # bounded compromise for long provisions and small retrieval limits.
    for chunk in chunks[position + 1:position + 4]:
        # Stop at a new section heading near the beginning of the next chunk.
        # A later heading can coexist with the end of the current provision.
        heading = HEADING_PATTERN.search(chunk["text"])
        if heading and heading.start() < 120:
            break
        yield chunk


def expand_adjacent_chunks(
    matches: list[dict],
    limit: int,
    all_chunks: dict | None = None,
) -> list[dict]:
    """Reserve one slot per seed, then fairly add adjacent supporting chunks.

    Unlike the previous implementation, this does not allow the first seed to
    consume every available slot before other selected sections are included.
    """
    if limit < 1 or not matches:
        return []

    seeds = []
    seen = set()
    for match in matches:
        if match["id"] not in seen:
            seeds.append(match)
            seen.add(match["id"])
        if len(seeds) == limit:
            return seeds

    if all_chunks is None:
        all_chunks = get_collection().get(include=["documents", "metadatas"])
    by_source, positions = _ordered_chunks(all_chunks)
    expanded = list(seeds)
    streams = [iter(_continuation_chunks(seed, by_source, positions)) for seed in seeds]

    # Round-robin: each requested section gets an opportunity for context.
    while len(expanded) < limit and streams:
        remaining = []
        progress = False
        for stream in streams:
            if len(expanded) >= limit:
                break
            for chunk in stream:
                if chunk["id"] not in seen:
                    expanded.append(chunk)
                    seen.add(chunk["id"])
                    progress = True
                    remaining.append(stream)
                    break
            # Exhausted streams are not reused.
        if not progress:
            break
        streams = remaining
    return expanded


def semantic_search(question: str, limit: int = 5) -> list[dict]:
    """Retrieve section headings and balanced continuations, or semantic matches."""
    if not question or not question.strip():
        raise ValueError("Search question cannot be empty.")
    if limit < 1:
        raise ValueError("Search limit must be positive.")

    collection = get_collection()
    total = collection.count()
    if total == 0:
        raise RuntimeError("ChromaDB collection is empty. Run python -m app.vectorstore first.")

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

    sections = extract_sections(question) or infer_sections(question)
    if not sections:
        return matches[:limit]

    # Full scan is necessary because the right section heading may be outside
    # the top semantic matches. Only one scan is performed per section query.
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

    selected = []
    selected_ids = set()
    # Every requested section gets a dedicated seed, as long as space exists.
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
        if len(selected) >= limit:
            return selected

    # Prefer section-heading seeds and their continuations over unrelated
    # semantic hits. If no heading is found, use semantic seeds instead.
    max_seeds = len(selected) if selected else min(limit, (limit + 1) // 2)

    def remaining_priority(match: dict):
        headings = [
            section_match_priority(match, section)
            for section in sections
            if find_section_heading(match["text"], section)
        ]
        if headings:
            return (0, min(headings))
        distance = match.get("distance")
        return (1, distance if distance is not None else float("inf"))

    for match in sorted(matches, key=remaining_priority):
        if len(selected) >= max_seeds:
            break
        if match["id"] not in selected_ids:
            selected.append(match)
            selected_ids.add(match["id"])

    expanded = expand_adjacent_chunks(selected, limit, all_chunks=all_chunks)
    # If adjacency is exhausted, return additional semantic matches instead
    # of unnecessarily returning fewer than the requested number of chunks.
    expanded_ids = {match["id"] for match in expanded}
    for match in sorted(matches, key=remaining_priority):
        if len(expanded) >= limit:
            break
        if match["id"] not in expanded_ids:
            expanded.append(match)
            expanded_ids.add(match["id"])
    return expanded


if __name__ == "__main__":
    total = index_documents()
    print(f"\nPersistent ChromaDB collection contains {total} chunks.")
