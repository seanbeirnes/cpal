from sentence_transformers import SentenceTransformer
from torch import Tensor

model = SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-cos-v1")

def extract_embeddings(text: str) -> Tensor:
    return model.encode(text)
