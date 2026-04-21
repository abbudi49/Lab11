"""
Lab 08 Setup Check
===================
Verifies that your CISC395/ environment is secure and your API key works.

Run from inside trip_notes/ with .venv active:
    python tests/check_api_setup.py

Checks:
  Part 1 — Security  (.gitignore, .env protection, .venv, requirements.txt)
  Part 2 — API       (calls tests/check_openrouter.py automatically)

Fix every failure before moving to Exercise 1.
Note: .gitignore, .env, .venv, requirements.txt all live at CISC395/ root (../).
"""

import os
import sys
import subprocess

# CISC395/ root is one level up from trip_notes/
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
ROOT = os.path.normpath(ROOT)  # trip_notes/tests/ → trip_notes/ → CISC395/

passed = 0
failed = 0
warnings = 0


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


def warn(label, hint=""):
    global warnings
    print(f"  \u26a0  {label}")
    if hint:
        print(f"       {hint}")
    warnings += 1


def p(path):
    """Return absolute path under CISC395/ root."""
    return os.path.join(ROOT, path)


# ── Part 1: Security ──────────────────────────────────────────────────────────

print("=== Lab 08 Setup Check ===")
print()
print("Part 1: Project Security  (checking CISC395/ root)")
print()

# .gitignore at CISC395/
if os.path.exists(p(".gitignore")):
    ok(".gitignore exists")
    content = open(p(".gitignore")).read()
    if ".env" in content:
        ok(".env is listed in .gitignore")
    else:
        fail(".env is NOT in .gitignore",
             "Add a line '.env' to CISC395/.gitignore, then commit it.")
    if ".venv" in content:
        ok(".venv/ is listed in .gitignore")
    else:
        warn(".venv/ not in .gitignore",
             "Add '.venv/' to CISC395/.gitignore.")
else:
    fail(".gitignore not found at CISC395/ root",
         "Run from CISC395/:  python Labs/Lab08/setup.py")

# .env not tracked by git
try:
    result = subprocess.run(
        ["git", "ls-files", ".env"],
        capture_output=True, text=True, cwd=ROOT
    )
    if result.stdout.strip() == "":
        ok(".env is NOT tracked by git")
    else:
        fail(".env IS tracked by git \u2014 your API key is exposed!",
             "Fix: git rm --cached .env  then commit the change.")
except FileNotFoundError:
    warn("git not found \u2014 cannot verify .env tracking")

# .env never in git history
try:
    result = subprocess.run(
        ["git", "log", "--all", "--oneline", "--", ".env"],
        capture_output=True, text=True, cwd=ROOT
    )
    if result.stdout.strip() == "":
        ok(".env has never been committed")
    else:
        fail(".env appears in git history \u2014 key may be permanently exposed",
             "Consider rotating your API key at openrouter.ai.")
except FileNotFoundError:
    pass

# .env exists locally
if os.path.exists(p(".env")):
    ok(".env file exists at CISC395/ root")
    env_text = open(p(".env")).read()
    if "OPENROUTER_API_KEY" in env_text or "GEMINI_API_KEY" in env_text:
        ok("API key entry found in .env")
    else:
        fail("No API key found in .env",
             "Add:  OPENROUTER_API_KEY=sk-or-v1-...  (or GEMINI_API_KEY=AIza-...)")
else:
    fail(".env not found at CISC395/ root",
         "Create CISC395/.env with your API key \u2014 never commit this file.")

# .venv at CISC395/
if os.path.isdir(p(".venv")):
    ok(".venv/ exists at CISC395/ root")
else:
    fail(".venv/ not found at CISC395/ root",
         "From CISC395/:  python -m venv .venv  then activate it.")

# requirements.txt at CISC395/
if os.path.exists(p("requirements.txt")):
    ok("requirements.txt exists")
    req = open(p("requirements.txt")).read().lower()
    for pkg in ["openai", "python-dotenv"]:
        if pkg in req:
            ok(f"  {pkg} in requirements.txt")
        else:
            fail(f"  {pkg} NOT in requirements.txt",
                 f"pip install {pkg}  then: pip freeze > requirements.txt")
else:
    fail("requirements.txt not found at CISC395/ root",
         "With .venv active: pip freeze > requirements.txt")

# ── Part 2: API Connectivity ──────────────────────────────────────────────────

print()
print("Part 2: API Connectivity")
print()

if failed > 0:
    print(f"  Skipping API check \u2014 fix the {failed} failure(s) above first.")
    print()
    print(f"Results: {passed} passed, {failed} failed, {warnings} warnings")
    sys.exit(1)

result = subprocess.run([sys.executable, "tests/check_openrouter.py"])

print()
if result.returncode == 0:
    print(f"Results: {passed} passed, {failed} failed, {warnings} warnings")
    print()
    print("All checks passed. Ready to start the exercises.")
    print("cd trip_notes \u2192 python tests/check_api_setup.py is your setup gate.")
else:
    print("OpenRouter check failed. Try the Gemini backup:")
    print("  python tests/check_gemini.py")
    print()
    print(f"Results: {passed} passed, {failed + 1} failed, {warnings} warnings")
    sys.exit(1)