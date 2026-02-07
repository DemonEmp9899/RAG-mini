"""
Main entry point for the RAG Policy QA project.

Flow:
1. Run ingestion & chunking (Phase 1)
2. Index embeddings into vector DB (Phase 2)
3. Interactive question-answering loop (Phase 3)
"""

from src.ingestion.pipeline import run_phase1
from src.retrieval.retriever import index_chunks
from src.qa.qa_pipeline import answer_question


def main():
    print("\n===== PHASE 1: INGESTION =====")
    run_phase1()

    print("\n===== PHASE 2: INDEXING =====")
    index_chunks()

    print("\n===== INTERACTIVE QA MODE =====")
    print("Ask a question based on the ingested documents.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        question = input("Your question: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Exiting QA system. Goodbye!")
            break

        if not question:
            print("Please enter a valid question.\n")
            continue

        answer = answer_question(question)
        print("\nAnswer:")
        print(answer)
        print("-" * 60)


if __name__ == "__main__":
    main()
