import chromadb
from chromadb.config import Settings

def get_vector_store(persist_dir: str = "data/processed/chroma_db"):
    client = chromadb.Client(
        Settings(
            persist_directory=persist_dir,
            anonymized_telemetry=False
        )
    )

    collection = client.get_or_create_collection(
        name="policy_docs"
    )

    return collection
