"""
Lab 07: Trip Notes — Project Setup
=====================================
Run this script from your CISC395 workspace root to create the
trip_notes/ project and download all required files.

Usage (from CISC395/ root):
    python Labs/Lab07/setup.py

OR download and run from CISC395/ root:
    curl -o setup.py https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab07/setup.py
    python setup.py
"""

import os
import sys
import urllib.request

BASE_URL = "https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab07/"

# Files to download into trip_notes/
DOWNLOADS = [
    ("tests/test_flow.py",              "tests/test_flow.py"),
    ("prompts/Lab07_Ex02_models.md",    "prompts/Lab07_Ex02_models.md"),
    ("prompts/Lab07_Ex03_storage.md",   "prompts/Lab07_Ex03_storage.md"),
    ("prompts/Lab07_Ex04_main.md",      "prompts/Lab07_Ex04_main.md"),
    ("prompts/Lab07_P2A_visited.md",    "prompts/Lab07_P2A_visited.md"),
    ("prompts/Lab07_P2B_stats.md",      "prompts/Lab07_P2B_stats.md"),
    ("prompts/Lab07_P2C_rating.md",     "prompts/Lab07_P2C_rating.md"),
]

EMPTY_SRC = ["src/main.py", "src/models.py", "src/storage.py"]


def check_location():
    """Warn if this looks like it is being run from inside Labs/Lab07/ instead of CISC395/."""
    cwd = os.getcwd()
    if os.path.basename(cwd) in ("Lab07", "Labs"):
        print("WARNING: It looks like you are running this from inside the Labs/ folder.")
        print(f"  Current directory: {cwd}")
        print("  Please run from your CISC395 workspace root instead:")
        print("  cd ../.." if os.path.basename(cwd) == "Lab07" else "  cd ..")
        print("  python Labs/Lab07/setup.py")
        sys.exit(1)


def setup():
    check_location()

    root = "trip_notes"

    if os.path.exists(root):
        print(f"'{root}/' already exists.")
        print("To re-download tests and prompts only, run:")
        print("  python Labs/Lab07/setup.py --refresh")
        return

    print(f"Creating {root}/ in: {os.getcwd()}")
    print()

    # Create directories
    for d in ["src", "data", "tests", "prompts"]:
        os.makedirs(os.path.join(root, d), exist_ok=True)

    # Create empty source files
    for f in EMPTY_SRC:
        open(os.path.join(root, f), "w").close()

    # Create requirements.txt and README.md
    open(os.path.join(root, "requirements.txt"), "w").close()
    with open(os.path.join(root, "README.md"), "w") as f:
        f.write("# Trip Notes\n")

    print("Downloading lab files into trip_notes/...")

    failed = []
    for remote, local in DOWNLOADS:
        dest = os.path.join(root, local)
        url = BASE_URL + remote
        try:
            urllib.request.urlretrieve(url, dest)
            print(f"  ✓  trip_notes/{local}")
        except Exception as e:
            print(f"  ✗  trip_notes/{local}  ({e})")
            failed.append((dest, url))

    print()
    if failed:
        print("Some downloads failed. Retry manually:")
        for dest, url in failed:
            print(f"  curl -o {dest} {url}")
        print()

    print("Done! Your project is at: trip_notes/")
    print()
    print("Next steps (both terminals):")
    print("  cd trip_notes")
    print("  Terminal 2: python tests/test_flow.py   (expect import errors — normal)")
    print("  Terminal 1: launch your AI, then type:")
    print("    Please read and follow the instructions in @prompts/Lab07_Ex02_models.md")


def refresh():
    """Re-download tests and prompts without recreating the project."""
    root = "trip_notes"
    if not os.path.exists(root):
        print("trip_notes/ not found. Run without --refresh first.")
        sys.exit(1)

    print(f"Refreshing tests/ and prompts/ in trip_notes/...")
    for remote, local in DOWNLOADS:
        dest = os.path.join(root, local)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        url = BASE_URL + remote
        try:
            urllib.request.urlretrieve(url, dest)
            print(f"  ✓  trip_notes/{local}")
        except Exception as e:
            print(f"  ✗  {local}  ({e})")


if __name__ == "__main__":
    if "--refresh" in sys.argv:
        check_location()
        refresh()
    else:
        setup()
