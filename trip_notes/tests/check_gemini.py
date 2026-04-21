"""
Gemini API Key Check (Backup Option)
======================================
Verifies that GEMINI_API_KEY is set and working via the OpenAI-compatible endpoint.

Free tier: 15 requests/min — enough for lab use.

Run from inside trip_notes/ with .venv active:
    python tests/check_gemini.py

API key must be in CISC395/.env (one level above trip_notes/).
"""

import os
import sys
import time

try:
    from dotenv import load_dotenv, find_dotenv
except ImportError:
    print("\u2717  python-dotenv not installed.")
    print("   From CISC395/:  pip install python-dotenv")
    sys.exit(1)

try:
    from openai import OpenAI
    import openai
except ImportError:
    print("\u2717  openai not installed.")
    print("   From CISC395/:  pip install openai")
    sys.exit(1)

# find_dotenv() searches upward from CWD (trip_notes/) and finds CISC395/.env
load_dotenv(find_dotenv())

print("=== Gemini API Key Check (Backup) ===")
print()

key = os.getenv("GEMINI_API_KEY")
if not key:
    print("\u2717  GEMINI_API_KEY not found.")
    print("   Add to CISC395/.env:")
    print("       GEMINI_API_KEY=AIza-your-key-here")
    print()
    print("   Get a free key at: https://aistudio.google.com")
    print("   Click 'Get API key' \u2192 'Create API key'")
    sys.exit(1)

print(f"\u2713  Key found: {key[:12]}...")

MODEL = "gemini-2.5-flash-preview-04-17"

client = OpenAI(
    api_key=key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

print(f"   Model: {MODEL}")
print("   Sending test request...")
print()

try:
    start = time.time()
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "Reply with exactly three words: API test successful"}
        ],
        max_tokens=20,
        temperature=0.0,
    )
    elapsed = time.time() - start
    text = response.choices[0].message.content.strip()

    print(f"\u2713  Response ({elapsed:.1f}s): {text}")
    print(f"\u2713  Model: {MODEL}")
    print()
    print("\u2713  Free tier \u2014 no charges.")
    print("   Note: limit is 15 req/min. If you see rate limit errors, wait 1 minute.")
    print()
    print("Your Gemini API key is working. Ready to use as a Lab 08 backup.")
    print()
    print("\u2500" * 50)
    print("To use Gemini in src/ai_assistant.py, replace the client block with:")
    print()
    print('    from dotenv import load_dotenv, find_dotenv')
    print('    load_dotenv(find_dotenv())')
    print()
    print('    client = OpenAI(')
    print('        api_key=os.getenv("GEMINI_API_KEY"),')
    print('        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",')
    print('    )')
    print('    MODEL = "gemini-2.5-flash-preview-04-17"')

except openai.AuthenticationError:
    print("\u2717  Authentication failed.")
    print("   Your API key is invalid or expired.")
    print("   Get a new key at: https://aistudio.google.com")
    sys.exit(1)

except openai.RateLimitError:
    print("\u2717  Rate limit hit (15 req/min).")
    print("   Wait 1 minute and try again.")
    sys.exit(1)

except openai.APIConnectionError as e:
    print(f"\u2717  Connection error: {e}")
    print("   Check your internet connection.")
    sys.exit(1)

except Exception as e:
    print(f"\u2717  Unexpected error: {e}")
    print("   The model name or endpoint may have changed.")
    print("   Check: https://ai.google.dev/gemini-api/docs/openai")
    sys.exit(1)
