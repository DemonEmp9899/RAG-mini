from src.ingestion.pipeline import run_phase1
from src.retrieval.retriever import index_chunks
from src.qa.qa_pipeline import answer_question


EVAL_QUESTIONS = [
    # Answerable
    "What is the refund window for products purchased on the platform?",
    "What conditions must be met to be eligible for a refund?",
    "Which items are explicitly marked as non-refundable?",
    "What happens if a subscription is cancelled halfway through a billing cycle?",
    "Are emergency service cancellations always fully refunded?",
    "What is the refund policy for international orders?",
    "Are refunds processed on weekends or holidays?"
]


def ask_score(metric_name: str) -> str:
    while True:
        score = input(f"{metric_name} (✅ / ⚠️ / ❌): ").strip()
        if score in {"✅", "⚠️", "❌"}:
            return score
        print("Please enter one of: ✅  ⚠️  ❌")


def run_evaluation():
    print("\n===== PHASE 1: INGESTION =====")
    run_phase1()

    print("\n===== PHASE 2: INDEXING =====")
    index_chunks()

    print("\n===== PHASE 4: MANUAL EVALUATION =====")

    results = []

    for i, question in enumerate(EVAL_QUESTIONS, start=1):
        print("\n" + "=" * 80)
        print(f"Q{i}: {question}")

        answer = answer_question(question)

        print("\nModel Answer:")
        print(answer)

        print("\n--- Evaluation ---")
        accuracy = ask_score("Accuracy")
        hallucination = ask_score("Hallucination avoidance")
        clarity = ask_score("Answer clarity")

        results.append({
            "question": question,
            "answer": answer,
            "accuracy": accuracy,
            "hallucination_avoidance": hallucination,
            "clarity": clarity
        })

    print("\n===== EVALUATION SUMMARY =====")
    for r in results:
        print("\nQuestion:", r["question"])
        print("Accuracy:", r["accuracy"])
        print("Hallucination avoidance:", r["hallucination_avoidance"])
        print("Answer clarity:", r["clarity"])

    print("\nEvaluation complete. You can now record these results in evaluation.md.")


if __name__ == "__main__":
    run_evaluation()