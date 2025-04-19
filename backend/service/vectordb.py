import os
import sys

from dotenv import load_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone
from model.match import Match, Metadata

DIMENSIONS = 384
MAX_BATCH_SIZE = 100

load_dotenv()

INDEX_NAME = os.environ['VECTOR_DB_INDEX_NAME']
pc = Pinecone(api_key=os.environ['VECTOR_DB_API_KEY'])

if not pc.has_index(INDEX_NAME):
    sys.exit(1)

INDEX_HOST = pc.describe_index(name=INDEX_NAME)["host"] 
pc_index = pc.Index(host=INDEX_HOST)

def query_similar(embeddings: list[float]) -> list[Match]:
    results = pc_index.query(namespace=INDEX_NAME,
            vector=embeddings,
            top_k=5,
            include_metadata=True,
            include_values=False)


    matches = []
    for m in results.get("matches"):
        match = Match(id=m.get("id"),metadata=Metadata(**m.get("metadata")), score=m.get("score"))
        matches.append(match)
    return matches

def get_chunk(id: str) -> list[Match]:
    results = pc_index.query(namespace=INDEX_NAME, id=id, top_k=1, include_metadata=True, include_values=False)

    matches = []
    for m in results.get("matches"):
        match = Match(id=m.get("id"),metadata=Metadata(**m.get("metadata")), score=m.get("score"))
        matches.append(match)
    return matches

