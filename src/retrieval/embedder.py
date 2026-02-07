from sentence_transformers import SentenceTransformer

# Lightweight, widely used model
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text: str):
    """
    Generate embedding locally without any API calls.
    """
    return model.encode(text, normalize_embeddings=True).tolist()
