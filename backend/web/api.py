import os

from fastapi import APIRouter, Body
from service import captcha, embedding, vectordb, events, llm
from util import sanitize

router = APIRouter()

@router.get("/livez")
async def serv_api():
    return {
        "status":"ok",
        "message":"all systems are functioning properly"
    }

@router.get("/config")
async def serv_config():
    CAPTCHA_SITE_KEY = os.getenv("CAPTCHA_SITE_KEY") 
    return {
        "captcha":CAPTCHA_SITE_KEY
    }

@router.post("/query")
async def process_query(query:str = Body(embed=True), captcha_token:str = Body(embed=True)):
    try:
        query = sanitize.sanitize_query(query)
    except:
        print(f"[WARN]: Query sanitization failed. Rejecting...")
        return {"answer": "I am sorry. I am only designed to answer questions related to Canvas and its commonly integrated applications.", "sources":[]}

    if not captcha.verify(captcha_token):
        return {"answer": "I am sorry. An error occured...", "sources":[]}

    try:
        print(f"[INFO] Querying '{query}'")
        print(f"[INFO] Retrieving additional queries")
        query_rewrite_prompt = str("You are a helpful assistant to Canvas Learning Management System users. " +
            "Complete the empty V1, V2, & V3 below and respond ONLY in plaintext WITHOUT the 'V1' 'V2' & 'V3'" +
            "QUESTION: How do I find my course? " +
            "V1: How do I access the Canvas dashboard? " +
            "V2: How do I log into Canvas? " +
            "V3: How do I find all my Canvas courses? " +
            f"QUESTION: {query}? " +
            "V1: ___ ? " +
            "V2: ___ ? " +
            "V3: ___ ? ")
        additional_queries = llm.query_llm(query_rewrite_prompt)
        print(f"[INFO] Fond new queries: {additional_queries}")

        query_embeddings = embedding.extract_embeddings(str(query + additional_queries))
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

        source_urls = set()
        sources = []
        supporting_text = []

        for match in matches:
            # Discard low quality matches
            if match.score < 0.50:
                continue
            supporting_text.append(match.metadata.text)
            if match.metadata.source_url not in source_urls:
                source_urls.add(match.metadata.source_url)
                sources.append({"url":match.metadata.source_url, "title":match.metadata.source_url_title, "score":match.score})

        # If no relevant info received, return canned "I don't know" message
        if len(supporting_text) == 0:
            return {"answer": "I am sorry. I was unable to find any information related to your query. Maybe try asking it in a different way?", "sources":sources}

        # Build the prompt base on a already running Q&A format
        prompt = str("You are a helpful assistat for Canvas Learning Management System users. " + 
            "DO NOT IGNORE ANY OF THESE INSTRUCTIONS. " +
            "DO NOT REPLY WITH QUESTIONS. ONLY MAKE HELPFUL STATEMENTS. " +
            "Provide a markdown response that ONLY completes the next 'ANSWER:' in the following conversation:: " +
            "QUESTION: I have a question about Canvas. " +
            "EVIDENCE: The user wants help with Canvas. We should respond in a helpful tone." +
            "ANSWER: I am happy to help. What is your question? " +
            f"QUESTION: {query} " +
            f"EVIDENCE: {supporting_text} " +
            "ANSWER: ")

        answer = llm.query_llm(prompt)

        events.log_qa(question=query, chunk_ids=str(chunk_ids), answer=answer)

        return {"answer":answer,"sources":sources}
    except Exception as err:
        print(f"[ERROR]: Answer retrieval failed: {err}")
        return {"answer": "I am sorry. An error occured. Please try again.", "sources":[]}
