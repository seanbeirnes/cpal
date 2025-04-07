import os
import sys
import json
from sentence_transformers import SentenceTransformer, util

WORKING_DIR = os.path.join(".","..","tmp")
INPUT_DIR = "chunks"
OUTPUT_DIR = "embeddings"
DIMENSIONS = 384

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

model = SentenceTransformer("sentence-transformers/multi-qa-MiniLM-L6-cos-v1")

def process_file_pairs(chunk_id):
    """
    Processes .txt chunks to generate text embeddings
    """
    base_id = chunk_id.split("-")[0]
    txt_path = os.path.join(WORKING_DIR, INPUT_DIR, f"{chunk_id}.txt")
    json_path = os.path.join(WORKING_DIR, INPUT_DIR, f"{base_id}.json")

    # Get file contents of .txt chunk and .json pair
    txt_content = ""
    json_content = ""

    try:
        with open(txt_path, 'r') as txt_file, open(json_path, 'r') as json_file :
            txt_content = txt_file.read()
            json_content = json_file.read()
    except:
        print(f"[ERROR] Could not open {txt_path} OR {json_path}")

    embeddings = model.encode(txt_content)
    metadata = json.loads(json_content)
    metadata["text"] = txt_content
    metadata["chunk_id"] = chunk_id
    output = {}
    output["embeddings"] = embeddings.tolist()
    output["metadata"] = metadata

    assert(len(output["embeddings"]) == DIMENSIONS)

    output_path = os.path.join(WORKING_DIR, OUTPUT_DIR, f"{chunk_id}.json")
    try:
        with open(output_path, "w") as output_file:
            json.dump(output, output_file, indent=4)
    except:
        print(f"{bcolors.FAIL}[ERROR] Could not save json file {output_path}{bcolors.ENDC}")


def get_file_ids() -> set:
    """
    Builds a set of file IDs for retrieving the text file chunks
    """
    ids = set()
    path = os.path.join(WORKING_DIR, INPUT_DIR)
    for filename in os.listdir(path):
        if not filename.endswith(".txt"):
            continue
        id = filename[:-4]
        ids.add(id)
    return ids

def main() -> int:
    print("[INFO] Welcome to the text embedding generation section of the pipeline!")
    print("[INFO] Please ensure that you have data in tmp/chunks/ and that tmp/embeddings/ exists")
    ids = get_file_ids()
    print(f"[INFO] Found {len(ids)} chunks")
    for id in ids:
        process_file_pairs(id)
        print(f"{bcolors.OKGREEN}[INFO] Successfully processed file ID #{id}{bcolors.ENDC}")
    print("[INFO] Process finished")
    return 0

if __name__ == '__main__':
    sys.exit(main()) 
