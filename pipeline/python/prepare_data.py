import sys
import os
import re
import shutil

import markdown
from bs4 import BeautifulSoup

WORKING_DIR = os.path.join(".","..","tmp")
INPUT_DIR = "raw"
OUTPUT_DIR = "chunks"

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

def clean_content(text) -> str:
    """
    Cleans markdown text by removing:
    - User @mentions
    - URLs (but keeps descriptive text)
    """
    # Remove user @mentions
    user_mention_regex = re.compile(r"\[@.+?\]\(\/t5\/user\/viewprofilepage\/user-id\/\d+\)", re.MULTILINE)
    cleaned_text = user_mention_regex.sub('', text)

    # Remove urls, but keep descriptive text of the url
    url_regex = re.compile(r"\[((?:[^\[\]]|\[[^\[\]]+\])+)\]\([^\)]+\)", re.MULTILINE)
    cleaned_text = url_regex.sub(r"\1", cleaned_text)

    # Ensure there are no left over escaped brackets from markdown links
    cleaned_text = cleaned_text.replace("\\[", "")
    cleaned_text = cleaned_text.replace("\\]", "")

    return cleaned_text

def chunk_content(text) -> list[str]:
    """
    Chunks content by markdown headings to preserve semantics
    """
    chunks = []
    current_chunk = ""
    for line in text.splitlines():
        if re.match(r"^#+\s", line):
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def remove_markdown(text) -> str:
    """
    Removes markdown and converts to plain text
    """
    html = markdown.markdown(text)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.get_text()

def process_file_pairs(id):
    """
    Processes file pairs of .json and .md raw data
    """
    md_path = os.path.join(WORKING_DIR, INPUT_DIR, f"{id}.md")
    json_path = os.path.join(WORKING_DIR, INPUT_DIR, f"{id}.json")

    # Get file contents of .json and .md pair
    md_content = ""
    json_content = ""
    try:
        with open(md_path, 'r') as md_file, open(json_path, 'r') as json_file :
            md_content = md_file.read()
            json_content = json_file.read()
    except:
        print(f"[ERROR] Could not open {md_path} OR {json_path}")

    md_content = clean_content(md_content)
    chunks = chunk_content(md_content)

    assert(len(chunks) != 0, "No chunks were returned")

    # Remove markdown from each chunk and save it
    for i, chunk in enumerate(chunks):
        chunk = remove_markdown(chunk)
        chunk_path = os.path.join(WORKING_DIR, OUTPUT_DIR, f"{id}-{i}.txt")
        try:
            with open(chunk_path, 'w') as out_file:
                out_file.write(chunk)
                # print(f"[INFO] Saved chunk to {chunk_path}")
        except:
            print(f"{bcolors.FAIL}[ERROR] Could not output file {chunk_path}{bcolors.ENDC}")
            print("[INFO] Are you sure tmp/chunks/ exists?")

    new_json_path = os.path.join(WORKING_DIR, OUTPUT_DIR, f"{id}.json")
    shutil.copyfile(json_path, new_json_path)

def get_file_ids() -> set:
    """
    Builds a set of file IDs for retrieving the markdown and json files later
    """
    ids = set()
    path = os.path.join(WORKING_DIR, INPUT_DIR)
    for filename in os.listdir(path):
        if not filename.endswith(".md"):
            continue
        id = filename[:-3]
        ids.add(id)
    return ids

def main() -> int:
    print("[INFO] Welcome to the data preparation section of the pipeline!")
    print("[INFO] Please ensure that you have data in tmp/raw/ and that tmp/chunks/ exists")
    ids = get_file_ids()
    print(f"[INFO] Found {len(ids)} '.md' and '.json' file pairs")
    for id in ids:
        process_file_pairs(id)
        print(f"{bcolors.OKGREEN}[INFO] Successfully processed file pair ID #{id}{bcolors.ENDC}")
    print("[INFO] Process finished")
    return 0

if __name__ == '__main__':
    sys.exit(main()) 
