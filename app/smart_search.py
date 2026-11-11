
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.records import load_records


def smart_search(query: str, limit: int = 10):
    """Rank traffic records by relevance using TF-IDF and cosine similarity."""

    if not query or not query.strip():
        return []

    records = load_records()

    if not records:
        return []

    documents = []

    for record in records:
        text = " ".join(
            str(record.get(field) or "")
            for field in ("section", "offence", "legal_text", "other_action")
        )
        documents.append(text)

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )

    document_vectors = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query.strip()])

    similarity_scores = cosine_similarity(
        query_vector,
        document_vectors
    ).flatten()

    ranked_indices = similarity_scores.argsort()[::-1]

    results = []

    for index in ranked_indices:
        score = float(similarity_scores[index])

        if score <= 0:
            continue

        result = records[index].copy()
        result["similarity_score"] = round(score, 4)

        results.append(result)

        if len(results) >= limit:
            break

    return results
