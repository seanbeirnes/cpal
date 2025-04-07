import os
import sys
import json

from dotenv import load_dotenv

from sentence_transformers import SentenceTransformer, util
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec

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
    sys.exit(1)

INDEX_HOST = pc.describe_index(name=INDEX_NAME)["host"] 
pc_index = pc.Index(host=INDEX_HOST)

model = SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-cos-v1")

def main() -> int:
    print("[INFO] Welcome to the stored embedding tester!")
    print("[INFO] Please ensure that you have embeddings stored in the vector database")
    while True:
        question = input("Enter a question: ")
        if question == "exit":
            break
        query_embeddings = model.encode(question)
        res = pc_index.query(namespace=INDEX_NAME,
                    vector=query_embeddings,
                    top_k=5,
                    include_metadata=True,
                    include_values=False)
        print(res)
        print()

    return 0

if __name__ == '__main__':
    sys.exit(main()) 
