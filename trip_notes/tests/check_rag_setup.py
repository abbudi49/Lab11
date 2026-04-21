"""
Lab 09 — RAG Setup Check
Run from trip_notes/: python tests/check_rag_setup.py
"""

import sys
from pathlib import Path

PASSED = 0
FAILED = 0


def check(label, condition, fix=""):
    global PASSED, FAILED
    if condition:
        print(f"  \u2713  {label}")
        PASSED += 1
    else:
        print(f"  \u2717  {label}")
        if fix:
            print(f"       Fix: {fix}")
        FAILED += 1


# ── Package checks ────────────────────────────────────────────────────────────

try:
    import chromadb
    check("chromadb installed", True)
except ImportError:
    check("chromadb installed", False, "pip install chromadb")

try:
    from sentence_transformers import SentenceTransformer
    check("sentence_transformers installed", True)
except ImportError:
    check("sentence_transformers installed", False, "pip install sentence-transformers")

try:
    import pypdf
    check("pypdf installed", True)
except ImportError:
    check("pypdf installed", False, "pip install pypdf")

# ── guides/ folder check ─────────────────────────────────────────────────────

guides_dir = Path("guides")
check("guides/ folder exists", guides_dir.exists(), "Run setup.py again or create guides/ manually")

if guides_dir.exists():
    guide_files = (
        list(guides_dir.glob("*.txt"))
        + list(guides_dir.glob("*.md"))
        + list(guides_dir.glob("*.pdf"))
    )
    count = len(guide_files)
    check(
        f"guides/ has files ({count} found)",
        count > 0,
        "Add at least one .txt, .md, or .pdf travel guide to guides/",
    )

# ── Summary ───────────────────────────────────────────────────────────────────

print()
if FAILED == 0:
    print(f"All checks passed. ({PASSED}/{PASSED})")
    print()
    print("Next: pip freeze > ../requirements.txt, then start Exercise 1.")
else:
    print(f"{PASSED} passed, {FAILED} failed. Fix the issues above and re-run.")
    sys.exit(1)
