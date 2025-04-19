from fastapi import APIRouter, Body
from service import embedding, vectordb, events

router = APIRouter()

@router.get("/livez")
def serv_api():
    return {
        "status":"ok",
        "message":"all systems are functioning properly"
    }

@router.post("/query")
def process_query(query:str = Body(embed=True)):
    query_embeddings = embedding.extract_embeddings(query)
    matches = vectordb.query_similar(query_embeddings.tolist())

    # If forum questions are returned, replace with answers
    chunk_ids = []
    for i, match in enumerate(matches):
        chunk_ids.append(match.id)
        if match.score < 0.75:
            continue
        if match.id.split("-")[1] != "0" or not match.metadata.text.startswith("Question"):
            continue

        print(f"[INFO] Found question chunk returned. Replacing chunk {match.id} with an answer")
        answers = vectordb.get_chunk(match.id.split("-")[0] + "-1")
        answer = answers[0]
        print(f"[INFO] Found answer chunk {answer.id}")
        chunk_ids.append(answer.id)
        matches[i].id = answer.id
        matches[i].metadata = answer.metadata

    events.log_qa(question=query, chunk_ids=str(chunk_ids), answer="to-do")

    return matches

