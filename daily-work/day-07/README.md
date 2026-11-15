
# Day 7 — PDF Chunking, Embeddings and Semantic Search

## Project: ChalanCheck

### Objective
Implement semantic search over official Motor Vehicles Act and Rules PDFs using sentence embeddings and ChromaDB.

## S1 — Document Chunking and Embeddings

Created `app/chunking.py` to extract text from PDF documents using PyMuPDF.

- Processed 4 legal PDF documents.
- Generated 1,726 text chunks.
- Used overlapping chunks to preserve context.
- Stored source filename, page number and document title for each chunk.

Created `app/embed.py` using the `all-MiniLM-L6-v2` sentence-transformer model.

- Generated 384-dimensional embeddings.
- Normalized embedding vectors.
- Implemented query embedding generation.

## S2 — ChromaDB Vector Store

Created `app/vectorstore.py` to store and retrieve legal document chunks.

- Used persistent ChromaDB storage in `data/chroma/`.
- Indexed 1,726 chunks.
- Implemented semantic similarity search.
- Added section-aware retrieval for legal section numbers.
- Improved retrieval for questions mentioning multiple sections.

## FastAPI Integration

Added the endpoint:

GET /search/semantic?q=<question>&limit=5

The endpoint returns matching document chunks with source, page number, title and similarity distance.

## Evaluation

Created `eval/evaluate_search.py` to evaluate semantic retrieval using 10 traffic challan questions.

Results are saved in:

`eval/search_results.md`

Verified that a question mentioning Sections 194D and 196 retrieves both legal provisions from the Motor Vehicles Act.

## Limitations

- Some searches may still return table-of-contents entries.
- Questions about police station opening hours cannot be reliably answered using the legal PDFs alone.
- Retrieved legal provisions must be verified before presenting penalties as definitive legal advice.

## Dependencies

- chromadb
- sentence-transformers
- pymupdf

## Commands

Check Python dependencies:

    python -m pip check

Rebuild the vector database when source documents change:

    python -m app.vectorstore

Run semantic search evaluation:

    python -m eval.evaluate_search

Start FastAPI:

    python -m uvicorn app.main:app --reload

API documentation:

    http://127.0.0.1:8000/docs

## Outcome

Completed PDF chunking, embedding generation, persistent vector indexing, semantic search, section-aware retrieval and FastAPI integration.
