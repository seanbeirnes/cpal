import os

from google import genai

LLM_API_KEY = os.getenv("LLM_API_KEY")

client = genai.Client(api_key=LLM_API_KEY)

def query_llm(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
    )
    return response.text

