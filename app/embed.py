
"""Generate local semantic embeddings for ChalanCheck."""

from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load the embedding model once and reuse it."""
    return SentenceTransformer(MODEL_NAME)


def embed_texts(texts: list[str]) -> np.ndarray:
    """Convert document chunks into normalized embedding vectors."""
    if not texts:
        return np.empty((0, 384), dtype=np.float32)

    model = get_embedding_model()

    return model.encode(
        texts,
        batch_size=32,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )


def embed_query(question: str) -> np.ndarray:
    """Generate a normalized embedding for a user question."""
    if not question.strip():
        raise ValueError("Question cannot be empty.")

    return embed_texts([question])[0]


if __name__ == "__main__":
    question = "What is the fine for riding without a helmet?"

    vector = embed_query(question)

    print("Embedding model:", MODEL_NAME)
    print("Question:", question)
    print("Vector dimensions:", len(vector))
    print("Vector norm:", round(float(np.linalg.norm(vector)), 4))
    print("First five values:", vector[:5])
