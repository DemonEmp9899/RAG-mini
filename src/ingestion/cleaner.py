import re

def clean_text(text: str) -> str:
    """
    Clean policy text while preserving meaning.
    """
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Remove repeated decorative characters
    text = re.sub(r"[-_=]{3,}", " ", text)

    # Strip leading/trailing spaces
    text = text.strip()

    return text
