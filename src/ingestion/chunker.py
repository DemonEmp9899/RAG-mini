import tiktoken

def get_tokenizer(model_name: str = "text-embedding-3-small"):
    return tiktoken.encoding_for_model(model_name)


def chunk_text(
    text: str,
    chunk_size: int = 400,
    overlap: int = 50,
    min_chunk_size: int = 100,  # 👈 IMPORTANT
    model_name: str = "text-embedding-3-small"
):
    tokenizer = get_tokenizer(model_name)
    tokens = tokenizer.encode(text)

    # If document is small, return single chunk
    if len(tokens) <= chunk_size:
        return [{
            "chunk_id": 0,
            "text": tokenizer.decode(tokens),
            "token_count": len(tokens)
        }]

    chunks = []
    start = 0
    chunk_id = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]

        # 🚫 Drop very small tail chunks
        if len(chunk_tokens) < min_chunk_size:
            break

        chunks.append({
            "chunk_id": chunk_id,
            "text": tokenizer.decode(chunk_tokens),
            "token_count": len(chunk_tokens)
        })

        chunk_id += 1
        start = end - overlap

    return chunks
