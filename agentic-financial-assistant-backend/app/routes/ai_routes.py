import os
import requests
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/ai", tags=["AI"])

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@router.post("/ask")
def ask_ai(payload: dict):
    query = payload.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Missing query")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json={
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": query}
            ]
        }
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Groq API error")

    data = response.json()
    return {"message": data["choices"][0]["message"]["content"]}
