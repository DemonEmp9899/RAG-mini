# Retrieval-Augmented Policy Question Answering System
Overview

This project implements a Retrieval-Augmented Generation (RAG) system for answering questions from company policy documents such as Refund Policy and Cancellation Policy.
The system retrieves relevant document sections and generates grounded, non-hallucinated answers, with explicit handling of missing or out-of-scope questions.

The primary focus of this project is on:

-Prompt engineering and iteration
-Retrieval grounding
-Hallucination avoidance
-Manual evaluation and reasoning

Setup Instructions
1. Clone the Repository
```
git clone <your-repo-url>
cd Rag-policy
```
2. Create and Activate Environment
```
conda create -n rag python=3.10
conda activate rag
```
3. Install Dependencies
```
pip install -r requirements.txt
```
4. Environment Variables

Create a .env file in the project root:
```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxx
```

Note:
-Embeddings are generated locally using sentence-transformers
-OpenRouter is used only for LLM inference

Running the Project
Run the complete pipeline with:
```
python main.py
```
This will:

-Ingest and chunk policy documents
-Index embeddings into the vector database
-Start an interactive QA session

Type exit to quit.

Architecture Overview

The system follows a modular Retrieval-Augmented Generation (RAG) architecture. Each stage of the pipeline is implemented in a dedicated module to ensure clarity and separation of concerns.

1. Ingestion & Chunking (Phase 1)

Purpose: Load raw policy documents, clean text, and split it into retrievable chunks.

Key files:

•src/ingestion/pipeline.py

  •Loads policy documents from data/raw/
  •Cleans and normalizes text
  •Applies tokenizer-based chunking with overlap
  •Saves processed chunks for downstream use

Why this matters:
Overlapping chunks preserve context while remaining within embedding limits.

2. Embedding & Vector Storage (Phase 2)

Purpose: Convert text chunks into vector embeddings and store them for semantic search.

Key files:

•src/retrieval/embedder.py

  •Generates embeddings using a local sentence-transformers model

•src/retrieval/retriever.py

  •Indexes embeddings into a Chroma vector database
  •Performs top-k semantic retrieval for user queries

Why this matters:
Local embeddings avoid API quota limits and make the system reproducible.

3. Retrieval-Augmented Generation (Phase 3)

Purpose: Retrieve relevant document chunks and generate grounded answers.

Key files:

•src/qa/qa_pipeline.py
  •Orchestrates retrieval and answer generation

•src/qa/answerer.py
  •Handles LLM calls via OpenRouter
  •Applies strict prompt rules to prevent hallucination

•src/qa/prompts.py
  •Stores prompt versions and supports prompt iteration

Why this matters:
Strict prompt design ensures the model answers only from retrieved context and handles missing information safely.

4. Evaluation (Phase 4)

Purpose: Measure answer quality and hallucination behavior.

Key files:

•eval/run_eval.py

  •Runs ingestion, indexing, and QA on a curated evaluation set
  •Prompts the evaluator to score responses manually

•eval/evaluation.md

  •Records evaluation results using a simple rubric (✅ / ⚠️ / ❌)

Why this matters:
Manual evaluation provides qualitative insight into model behavior, which is appropriate for small datasets.

5. Entry Point & User Interaction

Purpose: Provide a single command to run the system end-to-end.

Key file:

•main.py
  •Runs ingestion and indexing
  •Launches an interactive QA loop for custom queries

Prompt Engineering
Prompt v1 (Initial)
```
You are a helpful assistant answering questions based on the provided documents.

Context:
{context}

Question:
{question}

Answer:
```
Observed Issues:

  •No explicit restriction on outside knowledge
  •No guidance for missing information
  •Inconsistent answer structure
  •Occasional speculative responses

Prompt v2 (Improved – Final)
```
You are a document-grounded QA assistant.

Rules:
- Answer ONLY using the information in the context below.
- Do NOT use outside knowledge.
- If the answer is not present or only partially present, respond with:
  "The provided documents do not contain sufficient information to answer this question."

Context:
{context}

Question:
{question}

Answer format:
- Direct answer (1–2 sentences)
- Bullet points if listing facts
```

Prompt Iteration Explanation

The initial prompt did not explicitly prevent the model from using outside knowledge, which occasionally led to hallucinations.
The improved prompt introduces strict grounding rules, a mandatory fallback response, and a structured answer format, significantly reducing hallucinations and improving answer clarity.

Prompt Comparison (Bonus)
```
| Aspect                | Prompt v1 | Prompt v2      |
| --------------------- | --------- | -------------- |
| Grounding instruction | Implicit  | Explicit       |
| Missing-info handling | None      | Clear fallback |
| Output structure      | Free-form | Structured     |
| Hallucination risk    | Medium    | Low            |
| Evaluation clarity    | Low       | High           |
```

Example

Question: Does the refund policy mention international orders?

•Prompt v1 Output:
  “Refund policies may vary for international orders.” ❌

•Prompt v2 Output:
  “The provided documents do not contain sufficient information to answer this question.” ✅

Evaluation
Evaluation Method

•Manual evaluation (recommended for small datasets)
•Curated set of answerable, partially answerable, and unanswerable questions
•Metrics:
  •Accuracy
  •Hallucination avoidance
  •Answer clarity
•Rubric: ✅ / ⚠️ / ❌

Evaluation Summary
```
| Question Type                    | Accuracy | Hallucination Avoidance | Clarity |
| -------------------------------- | -------- | ----------------------- | ------- |
| Refund window                    | ✅        | ✅                       | ✅       |
| Refund eligibility               | ✅        | ✅                       | ✅       |
| Non-refundable items             | ✅        | ✅                       | ✅       |
| Subscription cancellation midway | ⚠️        | ✅                       | ✅       |
| Emergency service cancellations  | ❌        | ✅                       | ✅       |
| International refunds            | ❌        | ✅                       | ✅       |
| Weekend/holiday processing       | ❌        | ✅                       | ✅       |

```

Key Observation:
Out-of-scope questions consistently triggered safe refusals instead of hallucinated answers.

Edge Case Handling

No relevant documents retrieved
→ Safe fallback response

Question outside the knowledge base
→ Explicit refusal without speculation

Key Trade-offs

•Local embeddings were used to avoid API quota limits and improve reproducibility
•Manual evaluation was chosen over automated metrics due to small dataset size
•OCR was avoided to focus on RAG design rather than document digitization

Future Improvements

With more time, the system could be extended with:

•Chunk reranking for improved retrieval recall
•Query intent classification
•Structured JSON outputs
•Automated evaluation metrics
•Logging and tracing for deeper analysis

Final Notes

This project prioritizes clarity, grounding, and evaluation reasoning over UI or scale.
It demonstrates how careful prompt design and retrieval constraints can significantly reduce hallucinations in LLM-based systems.
