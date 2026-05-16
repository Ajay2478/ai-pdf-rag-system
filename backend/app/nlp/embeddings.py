"""
Embedding Service (Production-Ready)

- Uses sentence-transformers
- Supports batch processing (important for performance)
"""

from sentence_transformers import SentenceTransformer
from typing import List


# Load once (singleton)
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding for a single text input
    """
    return model.encode(text).tolist()


def generate_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings in batch (faster than single calls)
    """
    return model.encode(texts, show_progress_bar=False).tolist()