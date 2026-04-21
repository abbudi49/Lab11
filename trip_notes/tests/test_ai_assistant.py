"""
Lab 08 — Code Structure Check
===============================
Checks that src/ai_assistant.py has the correct interface.
Does NOT make real API calls.

Run from inside trip_notes/ after each exercise:
    python tests/test_ai_assistant.py
"""

import sys
import os
import inspect

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

passed = 0
failed = 0


def ok(label):
    global passed
    print(f"  \u2713  {label}")
    passed += 1


def fail(label, hint=""):
    global failed
    print(f"  \u2717  {label}")
    if hint:
        print(f"       \u2192 {hint}")
    failed += 1


print("=== ai_assistant.py Structure Check ===")
print()

# ── Import ────────────────────────────────────────────────────────────────────

try:
    import src.ai_assistant as ai
    ok("import src.ai_assistant")
except ImportError as e:
    fail("import src.ai_assistant", str(e))
    print()
    print("Cannot continue \u2014 fix the import error first.")
    print("Tell your AI: 'Fix the ImportError in src/ai_assistant.py'")
    sys.exit(1)

# ── After Exercise 1 ─────────────────────────────────────────────────────────

print()
print("--- Exercise 1: ask() and constants ---")

ok("ask() exists") if (hasattr(ai, "ask") and callable(ai.ask)) else \
    fail("ask() not found", "ai_assistant.py must define a function named ask()")

if hasattr(ai, "ask") and callable(ai.ask):
    sig = inspect.signature(ai.ask)
    params = list(sig.parameters)
    ok("ask() has user_message") if "user_message" in params else \
        fail("ask() missing user_message parameter")
    ok("ask() has system_prompt") if "system_prompt" in params else \
        fail("ask() missing system_prompt parameter",
             "Should be: ask(user_message, system_prompt=None, ...)")
    ok("ask() has temperature") if "temperature" in params else \
        fail("ask() missing temperature parameter",
             "Should be: ask(..., temperature=0.7, ...)")
    ok("ask() has max_tokens") if "max_tokens" in params else \
        fail("ask() missing max_tokens parameter",
             "Should be: ask(..., max_tokens=500)")

ok("TRAVEL_SYSTEM_PROMPT defined") if (
    hasattr(ai, "TRAVEL_SYSTEM_PROMPT") and
    isinstance(ai.TRAVEL_SYSTEM_PROMPT, str) and
    len(ai.TRAVEL_SYSTEM_PROMPT) > 20
) else fail("TRAVEL_SYSTEM_PROMPT missing or empty",
            "Define TRAVEL_SYSTEM_PROMPT as a non-empty string constant")

ok("MODEL defined") if (hasattr(ai, "MODEL") and isinstance(ai.MODEL, str)) else \
    fail("MODEL not defined", "Add:  MODEL = 'openrouter/free'")

ok("client defined") if hasattr(ai, "client") else \
    fail("client not found", "Create a module-level OpenAI client named 'client'")

# ── After Exercise 4 ─────────────────────────────────────────────────────────

print()
print("--- Exercise 4: generate_trip_briefing() ---")

if hasattr(ai, "generate_trip_briefing") and callable(ai.generate_trip_briefing):
    ok("generate_trip_briefing() exists")
    sig2 = inspect.signature(ai.generate_trip_briefing)
    params2 = list(sig2.parameters)
    ok("has city parameter") if "city" in params2 else \
        fail("missing city parameter",
             "Signature should be: generate_trip_briefing(city, country, notes=None)")
    ok("has country parameter") if "country" in params2 else \
        fail("missing country parameter")
    ok("has notes parameter (optional)") if "notes" in params2 else \
        fail("missing notes parameter",
             "Add: notes: list = None  — pass destination notes for personalized briefing")
else:
    print("  \u2014  generate_trip_briefing() not found (complete Exercise 4 first)")

# ── Summary ───────────────────────────────────────────────────────────────────

print()
print(f"Results: {passed} passed, {failed} failed")

if failed == 0:
    print()
    print("Structure looks good.")
    print("Run 'python src/ai_assistant.py' to test a live API call.")
else:
    print()
    print("Share this output with your AI:")
    print("  'Fix the issues in tests/test_ai_assistant.py output.")
    print("   Do not modify the check script itself.'")
