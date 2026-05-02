def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    """
    Split text into overlapping chunks.

    chunk_size = max characters per chunk
    overlap = shared context between chunks
    """

    chunks = []

    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size

        chunk = text[start:end]
        chunks.append(chunk)

        # Move with overlap
        start += chunk_size - overlap

    return chunks