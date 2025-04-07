import os
import sys
import json

from dotenv import load_dotenv
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

WORKING_DIR = os.path.join(".","..","tmp")
INPUT_DIR = "embeddings"
DIMENSIONS = 384
MAX_BATCH_SIZE = 100

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

load_dotenv()

INDEX_NAME = os.environ['VECTOR_DB_INDEX_NAME']
pc = Pinecone(api_key=os.environ['VECTOR_DB_API_KEY'])

if not pc.has_index(INDEX_NAME):
    pc.create_index(
        name=INDEX_NAME,
        vector_type="dense",
        dimension=DIMENSIONS,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        ),
        deletion_protection="disabled",
        tags={
            "environment": "development"
        }
    )

INDEX_HOST = pc.describe_index(name=INDEX_NAME)["host"] 
pc_index = pc.Index(host=INDEX_HOST)

def get_vectors_from_file(embedding_id):
    """
    Processes .json embedding files to store in vector database
    """
    base_id = embedding_id.split("-")[0]
    json_path = os.path.join(WORKING_DIR, INPUT_DIR, f"{embedding_id}.json")

    data = {}
    try:
        with open(json_path, 'r') as json_file :
            data = json.load(json_file)
    except:
        print(f"[ERROR] Could not open {json_path}")

    embeddings = data["embeddings"]
    metadata = data["metadata"]

    assert(metadata["id"] == base_id)
    assert(len(embeddings) == DIMENSIONS)

    vectors = {}
    vectors["id"] = metadata["chunk_id"]
    vectors["values"] = embeddings
    del metadata["chunk_id"]
    del metadata["id"]
    vectors["metadata"] = metadata
    return vectors

def upload_vectors(vectors) -> int:
    try:
        # In the future, may use multiple namespaces
        pc_index.upsert(vectors=vectors, namespace=INDEX_NAME)
        print(f"{bcolors.OKGREEN}[INFO] Succesfully uploaded vector batch{bcolors.ENDC}")
        return len(vectors)
    except:
        print(f"{bcolors.FAIL}[ERROR] Upload of vector batch failed{bcolors.ENDC}")
        return 0

def get_file_ids() -> set:
    """
    Builds a set of file IDs for retrieving the text file chunks
    """
    ids = set()
    path = os.path.join(WORKING_DIR, INPUT_DIR)
    for filename in os.listdir(path):
        if not filename.endswith(".json"):
            continue
        id = filename[:-5]
        ids.add(id)
    return ids

def main() -> int:
    print("[INFO] Welcome to the embedding storage section of the pipeline!")
    print("[INFO] Please ensure that you have data in tmp/embeddings/")
    ids = get_file_ids()
    print(f"[INFO] Found {len(ids)} embeddings")
    print(f"[INFO] Now uploading embeddings in batch sizes of {MAX_BATCH_SIZE}\n")

    batch = []
    uploaded = 0

    for id in ids:
        vec = get_vectors_from_file(id)
        if len(batch) >= MAX_BATCH_SIZE:
            uploaded += upload_vectors(batch)
            print(f"{uploaded}/{len(ids)} processed...\r")
            batch = []
        batch.append(vec)
        
    # Upload remaining vecs in batch
    if len(batch) > 0:
        uploaded += upload_vectors(batch)
        print(f"{uploaded}/{len(ids)} processed...\r")

    print("[INFO] Process finished")
    return 0

if __name__ == '__main__':
    sys.exit(main()) 
