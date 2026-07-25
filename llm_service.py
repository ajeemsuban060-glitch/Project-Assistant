"""
llm_service.py - Groq Cloud (free tier) for Assistant's reasoning/Q&A.
"""
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

_client = None

SYSTEM_PROMPT = (
    "You are Assistant, a helpful voice assistant. Answer clearly and "
    "concisely since your answers are spoken aloud, not read on screen. "
    "Keep answers to 2-3 sentences unless the user asks for more detail."
)


def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not set in .env file")
        _client = Groq(api_key=api_key)
    return _client


def get_response(transcript: str) -> str:
    """
    Sends the transcript to Groq and returns the reply text.
    Raises on failure - caller (assistant_core.py) is responsible for
    catching this and falling back to a spoken error message.
    """
    client = get_client()
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": transcript},
        ],
        max_tokens=150,
        temperature=0.7,
    )
    return completion.choices[0].message.content