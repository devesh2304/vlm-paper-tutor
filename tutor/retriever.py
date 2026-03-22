from tutor.embedder import get_client, get_embedder, COLLECTION_NAME

def retrieve(query: str, top_k: int = 5) -> list:
    """
    Given a question, find the most relevant chunks from Qdrant.
    Returns a list of payloads ranked by similarity.
    """
    client = get_client()
    embedder = get_embedder()

    query_vector = embedder.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k
    ).points

    chunks = []
    for hit in results:
        chunk = hit.payload.copy()
        chunk["score"] = round(hit.score, 3)
        chunks.append(chunk)

    return chunks

def format_context(chunks: list) -> str:
    """Format retrieved chunks into a readable context string for the LLM."""
    context_parts = []

    for i, chunk in enumerate(chunks):
        if chunk["type"] == "section":
            context_parts.append(
                f"[Section: {chunk['title']}]\n{chunk['content'][:800]}"
            )
        elif chunk["type"] == "figure":
            context_parts.append(
                f"[Figure on page {chunk.get('page', '?')}]\nCaption: {chunk['caption']}"
            )
        elif chunk["type"] == "table":
            context_parts.append(
                f"[Table on page {chunk.get('page', '?')}]\n{chunk['content'][:400]}"
            )

    return "\n\n---\n\n".join(context_parts)