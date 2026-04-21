"""
Trip Notes — Progress Check
============================
Checks your project structure and verifies prerequisites for a given lab.
Does NOT make API calls or modify any files.

Run from inside trip_notes/ with .venv active:
    python tests/check_progress.py --lab 08
    python tests/check_progress.py --lab 09
    python tests/check_progress.py --lab 09 --env
    python tests/check_progress.py          (auto-detects highest lab to check)

--env  also checks CISC395/ environment (.env, .venv, .gitignore, requirements.txt)
"""

import sys
import os
import argparse
import inspect

# Make src/ importable when running from trip_notes/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

# CISC395/ root is one level above trip_notes/
ROOT = os.path.normpath(os.path.join(BASE_DIR, ".."))

# ── Output helpers ─────────────────────────────────────────────────────────────

passed = 0
failed = 0
skipped = 0


def ok(label):
    global passed
    print(f"  ✓  {label}")
    passed += 1


def fail(label, hint=""):
    global failed
    print(f"  ✗  {label}")
    if hint:
        print(f"       → {hint}")
    failed += 1


def skip(label):
    global skipped
    print(f"  —  {label}")
    skipped += 1


def section(title):
    print(f"\n[{title}]")


def r(path):
    """Absolute path under ROOT (CISC395/)."""
    return os.path.join(ROOT, path)


def b(path):
    """Absolute path under BASE_DIR (trip_notes/)."""
    return os.path.join(BASE_DIR, path)


# ── Lab 07 checks ─────────────────────────────────────────────────────────────

def check_lab07():
    section("Lab 07 — Project Structure")
    ok_so_far = True

    # File existence
    for fname in ["src/models.py", "src/storage.py", "src/main.py"]:
        if os.path.exists(b(fname)):
            ok(f"{fname} exists")
        else:
            fail(f"{fname} missing", f"Complete Lab 07 — Exercise for {fname}")
            ok_so_far = False

    if not ok_so_far:
        skip("Skipping import checks — fix missing files first")
        return False

    # models.py — Destination
    try:
        from src.models import Destination, TripCollection
        ok("import Destination, TripCollection")
    except ImportError as e:
        fail(f"Cannot import from src.models: {e}")
        return False

    try:
        d = Destination("Test", "Country", 100.0)
        ok("Destination instantiates with (name, country, budget)")
    except Exception as e:
        fail(f"Destination() failed: {e}")
        return False

    ok("Destination.notes is a list") if isinstance(d.notes, list) \
        else fail("Destination.notes is not a list",
                  "Use field(default_factory=list) in @dataclass")

    ok("Destination.date_added is set") if (hasattr(d, "date_added") and d.date_added) \
        else fail("Destination.date_added missing or empty",
                  "Set date_added automatically in __post_init__")

    d.add_note("test note")
    ok("Destination.add_note() appends to notes") if "test note" in d.notes \
        else fail("add_note() does not append to notes")

    # Two instances have independent notes
    d2 = Destination("Paris", "France", 500.0)
    ok("Two Destinations have independent notes lists") if d.notes != d2.notes \
        else fail("Notes lists are shared between instances",
                  "Use field(default_factory=list), not notes: list = []")

    # TripCollection
    try:
        col = TripCollection()
        ok("TripCollection instantiates")
    except Exception as e:
        fail(f"TripCollection() failed: {e}")
        return False

    col.add(d)
    ok("TripCollection.add() works") if len(col) == 1 \
        else fail("TripCollection.add() did not increase length")

    ok("TripCollection.get_all() returns list") if isinstance(col.get_all(), list) \
        else fail("get_all() does not return a list")

    ok("TripCollection.get_by_index(0) works") if col.get_by_index(0).name == "Test" \
        else fail("get_by_index(0) returned wrong item")

    ok("TripCollection.search_by_country() works") \
        if len(col.search_by_country("country")) >= 1 \
        else fail("search_by_country() returned no results",
                  "Make sure comparison is case-insensitive")

    # storage.py
    try:
        from src.storage import load_trips, save_trips
        ok("import load_trips, save_trips")
    except ImportError as e:
        fail(f"Cannot import from src.storage: {e}")
        return False

    # main.py — Q quit check
    main_text = open(b("src/main.py")).read()
    if '== "q"' in main_text or "== 'q'" in main_text:
        ok("main.py uses Q to quit (Lab 08 menu polish applied)")
    else:
        skip("main.py still uses number to exit (Lab 08 Step 7 will update this)")

    return True


# ── Lab 08 checks ─────────────────────────────────────────────────────────────

def check_lab08():
    section("Lab 08 — AI Assistant")

    if not os.path.exists(b("src/ai_assistant.py")):
        fail("src/ai_assistant.py missing", "Complete Lab 08 Exercise 1")
        return False

    try:
        import src.ai_assistant as ai
        ok("import src.ai_assistant")
    except ImportError as e:
        fail(f"Cannot import src.ai_assistant: {e}", "Fix the ImportError first")
        return False

    # ask()
    if hasattr(ai, "ask") and callable(ai.ask):
        ok("ask() exists")
        params = list(inspect.signature(ai.ask).parameters)
        ok("ask() has system_prompt") if "system_prompt" in params \
            else fail("ask() missing system_prompt parameter")
        ok("ask() has temperature") if "temperature" in params \
            else fail("ask() missing temperature parameter")
    else:
        fail("ask() not found in ai_assistant.py")

    # Constants
    ok("TRAVEL_SYSTEM_PROMPT defined") if (
        hasattr(ai, "TRAVEL_SYSTEM_PROMPT")
        and isinstance(ai.TRAVEL_SYSTEM_PROMPT, str)
        and len(ai.TRAVEL_SYSTEM_PROMPT) > 20
    ) else fail("TRAVEL_SYSTEM_PROMPT missing or too short")

    ok("MODEL defined") if (hasattr(ai, "MODEL") and isinstance(ai.MODEL, str)) \
        else fail("MODEL not defined", "Add:  MODEL = 'openrouter/free'")

    ok("client defined") if hasattr(ai, "client") \
        else fail("client not defined", "Create module-level OpenAI client named 'client'")

    # generate_trip_briefing() — optional until Ex 4
    if hasattr(ai, "generate_trip_briefing") and callable(ai.generate_trip_briefing):
        ok("generate_trip_briefing() exists")
        params2 = list(inspect.signature(ai.generate_trip_briefing).parameters)
        if "trip" in params2:
            ok("generate_trip_briefing() accepts Destination object (trip)")
        elif "city" in params2 and "country" in params2:
            ok("generate_trip_briefing() accepts (city, country, notes)")
        else:
            fail("generate_trip_briefing() signature unexpected",
                 "Should be: generate_trip_briefing(trip)  — Destination object")
    else:
        skip("generate_trip_briefing() not found (complete Lab 08 Exercise 4 first)")

    # main.py — [6] Ask AI
    main_text = open(b("src/main.py")).read()
    if '"6"' in main_text or "'6'" in main_text:
        ok("[6] Ask AI added to main.py")
    else:
        skip("[6] Ask AI not yet in main.py (complete Lab 08 Exercise 3)")

    return True


# ── Lab 09 checks ─────────────────────────────────────────────────────────────

def check_lab09():
    section("Lab 09 — RAG Document Search")

    # guides/ folder
    guides_path = b("guides")
    if os.path.isdir(guides_path):
        docs = [f for f in os.listdir(guides_path)
                if f.endswith((".txt", ".md", ".pdf"))]
        if docs:
            ok(f"guides/ folder has {len(docs)} document(s): {', '.join(docs[:3])}")
        else:
            fail("guides/ folder is empty",
                 "Add at least one .txt, .md, or .pdf travel guide file")
    else:
        fail("guides/ folder missing",
             "Create trip_notes/guides/ and add travel guide files")

    # src/rag.py
    if not os.path.exists(b("src/rag.py")):
        fail("src/rag.py missing", "Complete Lab 09 Exercise 2")
        return False

    try:
        import src.rag as rag
        ok("import src.rag")
    except ImportError as e:
        fail(f"Cannot import src.rag: {e}")
        return False

    for fn in ["build_index", "search_guides", "ensure_index"]:
        ok(f"rag.{fn}() exists") if hasattr(rag, fn) \
            else fail(f"rag.{fn}() missing")

    # rag_ask() in ai_assistant
    try:
        import src.ai_assistant as ai
        if hasattr(ai, "rag_ask") and callable(ai.rag_ask):
            ok("rag_ask() added to ai_assistant.py")
        else:
            skip("rag_ask() not yet in ai_assistant.py (complete Lab 09 Exercise 3)")
    except ImportError:
        skip("Cannot check rag_ask() — fix ai_assistant.py import first")

    # chroma_db
    if os.path.isdir(b("chroma_db")):
        ok("chroma_db/ exists (index has been built)")
    else:
        skip("chroma_db/ not found — run python src/rag.py to build the index")

    # main.py — [8] Search my guides
    main_text = open(b("src/main.py")).read()
    if '"8"' in main_text or "'8'" in main_text:
        ok("[8] Search my guides added to main.py")
    else:
        skip("[8] Search my guides not yet in main.py (complete Lab 09 Exercise 4)")

    if '== "r"' in main_text or "== 'r'" in main_text:
        ok("[R] Rebuild search index added to main.py")
    else:
        skip("[R] Rebuild index not yet in main.py (complete Lab 09 Exercise 4)")

    return True


# ── Lab 10 checks ─────────────────────────────────────────────────────────────

def check_lab10():
    section("Lab 10 — Function Calling + ReAct Agent")

    if not os.path.exists(b("src/tools.py")):
        fail("src/tools.py missing", "Complete Lab 10 Exercise 1")
        return False

    try:
        import src.tools as tools
        ok("import src.tools")
    except ImportError as e:
        fail(f"Cannot import src.tools: {e}")
        return False

    # Three tool functions
    for fn in ["budget_breakdown", "get_weather", "search_guides_tool"]:
        ok(f"{fn}() exists") if hasattr(tools, fn) and callable(getattr(tools, fn)) \
            else fail(f"{fn}() missing", "Complete Lab 10 Exercise 1")

    # TOOL_DEFINITIONS
    if hasattr(tools, "TOOL_DEFINITIONS") and isinstance(tools.TOOL_DEFINITIONS, list):
        ok(f"TOOL_DEFINITIONS defined ({len(tools.TOOL_DEFINITIONS)} tools)")
        ok("TOOL_DEFINITIONS has 3 entries") if len(tools.TOOL_DEFINITIONS) == 3 \
            else fail(f"TOOL_DEFINITIONS has {len(tools.TOOL_DEFINITIONS)} entries, expected 3")
    else:
        fail("TOOL_DEFINITIONS missing or not a list")

    # Quick smoke test of budget_breakdown (pure math, always safe to call)
    try:
        result = tools.budget_breakdown("Tokyo", 7, 1400)
        ok("budget_breakdown() returns a string") if isinstance(result, str) \
            else fail("budget_breakdown() did not return a string")
    except Exception as e:
        fail(f"budget_breakdown() raised an error: {e}")

    # Check get_weather exists and accepts city parameter
    if hasattr(tools, "get_weather"):
        import inspect
        params = list(inspect.signature(tools.get_weather).parameters)
        ok("get_weather() has city parameter") if "city" in params \
            else fail("get_weather() missing city parameter")

    # Check search_guides_tool exists and accepts query parameter
    if hasattr(tools, "search_guides_tool"):
        import inspect
        params = list(inspect.signature(tools.search_guides_tool).parameters)
        ok("search_guides_tool() has query parameter") if "query" in params \
            else fail("search_guides_tool() missing query parameter")

    # run_agent()
    if hasattr(tools, "run_agent") and callable(tools.run_agent):
        ok("run_agent() exists")
    else:
        skip("run_agent() not found (complete Lab 10 Exercise 2)")

    # main.py — [10] AI Travel Agent
    main_text = open(b("src/main.py")).read()
    if '"10"' in main_text or "'10'" in main_text:
        ok("[10] AI Travel Agent added to main.py")
    else:
        skip("[10] AI Travel Agent not yet in main.py (complete Lab 10 Exercise 3)")

    return True


# ── Environment check ───────────────────────────────────────────────────────��─

def check_env():
    section("Environment — CISC395/ root")

    ok(".gitignore exists") if os.path.exists(r(".gitignore")) \
        else fail(".gitignore missing",
                  "Create CISC395/.gitignore with .env and .venv/ entries")

    if os.path.exists(r(".gitignore")):
        content = open(r(".gitignore")).read()
        ok(".env in .gitignore") if ".env" in content \
            else fail(".env not listed in .gitignore — API key not protected!")
        ok(".venv/ in .gitignore") if ".venv" in content \
            else fail(".venv/ not listed in .gitignore")

    ok(".env exists") if os.path.exists(r(".env")) \
        else fail(".env missing", "Create CISC395/.env with your OPENROUTER_API_KEY")

    if os.path.exists(r(".env")):
        env_text = open(r(".env")).read()
        ok("API key entry in .env") \
            if ("OPENROUTER_API_KEY" in env_text or "GEMINI_API_KEY" in env_text) \
            else fail("No API key found in .env")

    ok(".venv/ exists") if os.path.isdir(r(".venv")) \
        else fail(".venv/ missing", "From CISC395/: python -m venv .venv")

    ok("requirements.txt exists") if os.path.exists(r("requirements.txt")) \
        else fail("requirements.txt missing",
                  "With .venv active: pip freeze > requirements.txt")

    if os.path.exists(r("requirements.txt")):
        req = open(r("requirements.txt")).read().lower()
        for pkg in ["openai", "python-dotenv"]:
            ok(f"{pkg} in requirements.txt") if pkg in req \
                else fail(f"{pkg} not in requirements.txt",
                          f"pip install {pkg}  then: pip freeze > requirements.txt")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Check Trip Notes progress before starting a lab."
    )
    parser.add_argument(
        "--lab", type=int, choices=[7, 8, 9, 10], default=None,
        help="Lab number to check prerequisites for (7, 8, 9, or 10)"
    )
    parser.add_argument(
        "--env", action="store_true",
        help="Also check CISC395/ environment (.env, .venv, .gitignore)"
    )
    args = parser.parse_args()

    # Auto-detect if no --lab given
    lab = args.lab
    if lab is None:
        if os.path.exists(b("src/tools.py")):
            lab = 10
        elif os.path.exists(b("src/rag.py")) or os.path.isdir(b("guides")):
            lab = 9
        elif os.path.exists(b("src/ai_assistant.py")):
            lab = 8
        else:
            lab = 7
        print(f"(No --lab specified — auto-detected: Lab {lab:02d})")

    print(f"\n=== Trip Notes Progress Check: Ready for Lab {lab:02d}? ===")

    if args.env:
        check_env()

    lab07_ok = check_lab07()

    if lab >= 8:
        if lab07_ok:
            check_lab08()
        else:
            print("\n[Lab 08 — AI Assistant]")
            print("  Skipped — fix Lab 07 issues first.")

    if lab >= 9:
        check_lab08_ok = not any(
            not os.path.exists(b(f))
            for f in ["src/ai_assistant.py", "src/models.py", "src/storage.py"]
        )
        if check_lab08_ok:
            check_lab09()
        else:
            print("\n[Lab 09 — RAG Document Search]")
            print("  Skipped — fix Lab 08 issues first.")

    if lab >= 10:
        if os.path.exists(b("src/rag.py")):
            check_lab10()
        else:
            print("\n[Lab 10 — Function Calling + ReAct Agent]")
            print("  Skipped — complete Lab 09 (src/rag.py) first.")

    # Summary
    print(f"\n{'─' * 45}")
    print(f"  ✓ {passed} passed   ✗ {failed} failed   — {skipped} skipped")
    print(f"{'─' * 45}")

    if failed == 0:
        print(f"\n  All checks passed. You're ready for Lab {lab + 1:02d}.")
        if not args.env:
            print("  Tip: run with --env to also verify your API environment.")
    else:
        print(f"\n  {failed} issue(s) found. Fix them before continuing.")
        print("  Show this output to your AI:")
        print(f'  "Fix the failing checks shown by tests/check_progress.py --lab {lab:02d}"')

    print()
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
