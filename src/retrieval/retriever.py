import json
from src.retrieval.embedder import generate_embedding
from src.retrieval.vector_store import get_vector_store


CHUNKS_PATH = "data/processed/chunks.json"


def index_chunks():
    collection = get_vector_store()

    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Indexing {len(chunks)} chunks...")

    for idx, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk["text"])

        collection.add(
            ids=[str(idx)],
            documents=[chunk["text"]],
            metadatas=[chunk["metadata"]],
            embeddings=[embedding]
        )

    print("Indexing complete.")


def retrieve(query: str, top_k: int = 3):
    collection = get_vector_store()

    query_embedding = generate_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


if __name__ == "__main__":
    index_chunks()
    
