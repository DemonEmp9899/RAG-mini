from src.retrieval.retriever import retrieve
from src.qa.answerer import generate_answer


def answer_question(question: str, top_k: int = 3):
    results = retrieve(question, top_k=top_k)

    documents = results.get("documents", [[]])[0]

    if not documents:
        return "No relevant information found in the provided documents."

    context = "\n\n".join(documents)
    return generate_answer(context, question)


if __name__ == "__main__":
    q = "What is the refund period?"
    print(answer_question(q))
