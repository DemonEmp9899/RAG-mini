import json
import os

from src.ingestion.loader import load_documents
from src.ingestion.cleaner import clean_text
from src.ingestion.chunker import chunk_text


RAW_DATA_DIR = "data/raw"
OUTPUT_PATH = "data/processed/chunks.json"


def run_phase1():
    documents = load_documents(RAW_DATA_DIR)
    all_chunks = []

    for doc in documents:
        cleaned_text = clean_text(doc["text"])
        chunks = chunk_text(cleaned_text)

        for chunk in chunks:
            all_chunks.append({
             "text": chunk["text"],
             "metadata": {
            **doc["metadata"],
            "chunk_id": chunk["chunk_id"],
            "token_count": chunk["token_count"]
         }
     })


    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)

    print(f"Phase 1 completed. Saved {len(all_chunks)} chunks.")


if __name__ == "__main__":
    run_phase1()
