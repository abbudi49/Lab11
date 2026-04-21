import os
from typing import Optional
from dotenv import load_dotenv, find_dotenv

# Load API keys from .env in project root
load_dotenv(find_dotenv())

# Preferred API key
API_KEY = os.environ.get("OPENROUTER_API_KEY") or os.environ.get("OPENAI_API_KEY")

# Lab 08 requirements: module-level client and MODEL
MODEL = "openrouter/free"

# Initialize client if key is available
client = None
if API_KEY:
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=API_KEY,
            base_url="https://openrouter.ai/api/v1",
        )
    except ImportError:
        client = None

TRAVEL_SYSTEM_PROMPT = (
    "You are a helpful, concise travel assistant. Answer travel-related questions clearly, "
    "give practical tips, and if asked provide packing suggestions. Be friendly and brief."
)


def _offline_response(prompt: str) -> str:
    # A simple deterministic offline response for testing and when API keys are missing.
    if "packing" in prompt.lower() or "pack" in prompt.lower():
        return "Overview: Short trip overview.\nPacking list: passport, charger, comfortable shoes."
    return "I'm running in offline mode — no API key configured or API call failed. Try setting OPENROUTER_API_KEY.\n" + (
        "Example answer: Visit local markets and try street food."
    )


def ask(
    user_message: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 500,
) -> str:
    """Ask the configured LLM for `user_message`.

    If no API key or client is configured, returns a harmless offline response.
    """
    system = system_prompt or TRAVEL_SYSTEM_PROMPT
    
    if not client:
        return _offline_response(user_message)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_message},
            ],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"API Error: {e}")
        # Any failure falls back to offline stub
        return _offline_response(user_message)


def generate_trip_briefing(city: str, country: str, notes: Optional[list[str]] = None) -> str:
    """Two-step briefing: overview then packing list.

    Uses `ask()` internally. When offline, returns simple templated output.
    """
    notes_text = "\nNotes: " + ", ".join(notes) if notes else ""
    q1 = f"Write a short overview for {city}, {country}.{notes_text}"
    overview = ask(q1, system_prompt=TRAVEL_SYSTEM_PROMPT, temperature=0.3)

    q2 = f"Given the overview below, produce a short packing list for a student traveler to {city}:\n\n{overview}"
    packing = ask(q2, system_prompt=TRAVEL_SYSTEM_PROMPT, temperature=0.3)

    return f"Overview:\n{overview}\n\nPacking list:\n{packing}"


if __name__ == "__main__":
    # Quick manual test when running this file directly
    print(generate_trip_briefing("Tokyo", "Japan", notes=["conference"]))


def rag_ask(question: str) -> str:
    """Ask using retrieval-augmented generation (RAG).

    This function searches local guides and asks the LLM to answer only from
    the returned chunks. If no chunks are available, it returns a helpful message.
    """
    try:
        from src.rag import search_guides
    except Exception:
        return "RAG support not available (missing src.rag)."

    # Increased n_results to 5 for more context
    chunks = search_guides(question, n_results=5)
    if not chunks:
        return "No guide content found. Add files to guides/ and rebuild the index."

    # Build a strict system prompt that confines the model to the provided chunks.
    sources = "\n\n---\n\n".join(chunks)
    
    # Custom system prompt for RAG that allows more detail
    system = (
        "You are a helpful travel guide assistant. "
        "Answer the user's question as thoroughly as possible using ONLY the information in the provided source chunks. "
        "Use the information provided to give a complete and helpful answer. "
        "If the answer is not contained in the chunks, respond: 'I don't know from the guides.'\n\n"
        "SOURCE CHUNKS:\n"
        + sources
    )

    return ask(question, system_prompt=system, temperature=0.0)
