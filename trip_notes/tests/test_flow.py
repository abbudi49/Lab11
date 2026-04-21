"""
Trip Notes — Integration Test
==============================
Provided by your instructor. Do NOT modify this file.

Run after completing Exercises 2, 3, and 4 (from inside trip_notes/):
    python tests/test_flow.py

All tests must pass before committing.
If tests fail, share the output with your AI and ask it to fix the issues.
"""

import sys
import os
import json

# Make src/ importable when running from trip_notes/ root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

PASSED = 0
FAILED = 0


def check(label, condition, hint=""):
    global PASSED, FAILED
    if condition:
        print(f"  ✓  {label}")
        PASSED += 1
    else:
        print(f"  ✗  {label}")
        if hint:
            print(f"     Hint: {hint}")
        FAILED += 1


def run_tests():
    global PASSED, FAILED
    PASSED = 0
    FAILED = 0

    print("\n=== Trip Notes — Integration Tests ===\n")

    # ── Imports ──────────────────────────────────────────────────────────────
    print("[ Imports ]")
    try:
        from src.models import Destination, TripCollection
        check("import Destination from src.models", True)
        check("import TripCollection from src.models", True)
    except ImportError as e:
        check("import from src.models", False, str(e))
        print("\n  Cannot continue — fix import errors in src/models.py first.")
        _print_summary()
        return

    try:
        from src.storage import load_trips, save_trips
        check("import load_trips, save_trips from src.storage", True)
    except ImportError as e:
        check("import from src.storage", False, str(e))
        print("\n  Cannot continue — fix import errors in src/storage.py first.")
        _print_summary()
        return

    # ── Destination ───────────────────────────────────────────────────────────
    print("\n[ Destination ]")
    d1 = Destination("Tokyo", "Japan", 1200.0)
    check("name field set correctly",    d1.name    == "Tokyo")
    check("country field set correctly", d1.country == "Japan")
    check("budget field set correctly",  d1.budget  == 1200.0)
    check("notes defaults to empty list", d1.notes == [],
          "Use field(default_factory=list), not notes: list = []")
    check("date_added is auto-set", bool(d1.date_added),
          "date_added should be set to today's date automatically")

    d1.add_note("Visit Shibuya")
    check("add_note() appends to notes", "Visit Shibuya" in d1.notes)

    d2 = Destination("Paris", "France", 2000.0)
    d2.add_note("See the Louvre")
    check("two Destinations have independent notes lists", d1.notes != d2.notes,
          "Each Destination needs its own list — use field(default_factory=list)")

    # ── TripCollection ────────────────────────────────────────────────────────
    print("\n[ TripCollection ]")
    col = TripCollection()
    check("new TripCollection is empty (len == 0)", len(col) == 0)

    col.add(d1)
    check("add() increases length to 1", len(col) == 1)
    col.add(d2)
    check("add() increases length to 2", len(col) == 2)

    all_trips = col.get_all()
    check("get_all() returns a list", isinstance(all_trips, list))
    check("get_all() has 2 items",    len(all_trips) == 2)

    results = col.search_by_country("japan")
    check("search_by_country() finds a match",        len(results) >= 1)
    check("search_by_country() is case-insensitive",  results[0].name == "Tokyo",
          "Compare with .lower() on both sides")

    empty = col.search_by_country("Germany")
    check("search_by_country() returns [] for no match", empty == [])

    item = col.get_by_index(0)
    check("get_by_index(0) returns first added item", item.name == "Tokyo")

    # ── Storage round-trip ────────────────────────────────────────────────────
    print("\n[ Storage ]")
    data_path = os.path.join(BASE_DIR, "data", "trips.json")

    # Remove any leftover file from a previous run
    if os.path.exists(data_path):
        os.remove(data_path)

    save_trips(col)
    check("save_trips() creates data/trips.json", os.path.exists(data_path),
          "Check that storage.py builds the path using BASE_DIR (not a relative path)")

    # Verify JSON is valid
    with open(data_path) as f:
        raw = json.load(f)
    check("trips.json contains 2 entries", len(raw) == 2)

    col2 = load_trips()
    check("load_trips() returns a TripCollection (not a plain list)",
          hasattr(col2, "get_all"),
          "load_trips() should return TripCollection, not list")
    check("loaded collection has 2 trips",   len(col2) == 2)
    check("loaded Destination has correct name",
          col2.get_by_index(0).name == "Tokyo")
    check("loaded Destination preserves notes",
          "Visit Shibuya" in col2.get_by_index(0).notes)

    # Cleanup — remove test data so it does not end up committed
    os.remove(data_path)
    check("test data cleaned up", not os.path.exists(data_path))

    _print_summary()


def _print_summary():
    print(f"\n{'─' * 40}")
    print(f"  Passed: {PASSED}    Failed: {FAILED}")
    if FAILED == 0:
        print("  All tests passed. Ready to commit.")
    else:
        print(f"  {FAILED} test(s) failed.")
        print()
        print("  Next step: show your AI this output and say:")
        print('  "Run tests/test_flow.py and fix all failing tests."')
    print(f"{'─' * 40}\n")


if __name__ == "__main__":
    run_tests()
