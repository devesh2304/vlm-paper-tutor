import os
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

load_dotenv()

COLLECTION_NAME = "papers"
VECTOR_SIZE = 384

# initialize local embedding model and Qdrant in-memory
embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = QdrantClient(":memory:")

def init_collection():
    """Create Qdrant collection if it doesn't exist."""
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE
            )
        )
        print(f"Collection '{COLLECTION_NAME}' created.")

def embed_paper(paper_data: dict):
    """Embed all sections, figures and tables from a paper into Qdrant."""
    init_collection()
    points = []

    # embed sections
    for section in paper_data["sections"]:
        if not section["content"].strip():
            continue
        text = f"{section['title']}: {section['content'][:1000]}"
        vector = embedder.encode(text).tolist()
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "type": "section",
                "title": section["title"],
                "content": section["content"][:2000],
                "paper": paper_data["title"]
            }
        ))

    # embed figure captions
    for fig in paper_data["figures"]:
        if not fig["caption"].strip():
            continue
        vector = embedder.encode(fig["caption"]).tolist()
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "type": "figure",
                "caption": fig["caption"],
                "page": fig["page"],
                "paper": paper_data["title"]
            }
        ))

    # embed tables
    for table in paper_data["tables"]:
        if not table["content"].strip():
            continue
        vector = embedder.encode(table["content"][:500]).tolist()
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector,
            payload={
                "type": "table",
                "content": table["content"][:2000],
                "page": table["page"],
                "paper": paper_data["title"]
            }
        ))

    if points:
        client.upsert(collection_name=COLLECTION_NAME, points=points)
        print(f"Embedded {len(points)} chunks into Qdrant.")

def get_client():
    return client

def get_embedder():
    return embedder