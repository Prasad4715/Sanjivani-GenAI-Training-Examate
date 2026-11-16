
"""Extract page-aware text chunks from ChalanCheck legal PDFs."""

from pathlib import Path
import hashlib

import pymupdf


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 250) -> list[str]:
    """Split text into overlapping chunks measured in characters."""
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("chunk_size must be positive and overlap must be smaller.")

    text = " ".join(text.split())
    if not text:
        return []

    chunks = []
    step = chunk_size - overlap

    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size]
        if chunk:
            chunks.append(chunk)
        if start + chunk_size >= len(text):
            break

    return chunks


def chunk_pdf(pdf_path: Path) -> list[dict]:
    """Extract chunks while retaining source, page and title metadata."""
    pdf_path = Path(pdf_path)
    chunks = []

    with pymupdf.open(pdf_path) as document:
        title = document.metadata.get("title") or pdf_path.stem.replace("_", " ").title()

        for page_index, page in enumerate(document):
            page_text = page.get_text("text")

            for chunk_index, text in enumerate(chunk_text(page_text)):
                chunk_id = hashlib.sha256(
                    f"{pdf_path.name}:{page_index}:{chunk_index}:{text}".encode("utf-8")
                ).hexdigest()

               
                chunks.append({
                    "id": chunk_id,
                    "text": text,
                    "source": pdf_path.name,
                    "page": page_index + 1,
                    "chunk_index": chunk_index,
                    "title": title,
                })


    return chunks


def chunk_all_documents(raw_dir: Path = RAW_DIR) -> list[dict]:
    """Chunk all PDFs in the raw document directory."""
    pdf_files = sorted(Path(raw_dir).glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found in {raw_dir}")

    all_chunks = []

    for pdf_path in pdf_files:
        document_chunks = chunk_pdf(pdf_path)
        all_chunks.extend(document_chunks)
        print(f"{pdf_path.name}: {len(document_chunks)} chunks")

    return all_chunks


if __name__ == "__main__":
    chunks = chunk_all_documents()

    print(f"\nTotal chunks: {len(chunks)}")

    if chunks:
        sample = chunks[0]
        print("\nSample chunk metadata:")
        print(f"ID: {sample['id'][:16]}...")
        print(f"Source: {sample['source']}")
        print(f"Page: {sample['page']}")
        print(f"Title: {sample['title']}")
        print(f"Text preview: {sample['text'][:150]}...")
