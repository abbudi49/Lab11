# Lab 07: Trip Notes — A Structured Project

**Course:** CISC 395 Applied Generative AI and LLM Applications
**Week:** 8 (first post-midterm lab)
**Points:** 100

---

## Overview

So far, all your Python projects have been single files. In this lab you will build your first **multi-file, structured Python project** — a Trip Notes command-line app that lets you save and manage travel destinations.

You will use your terminal AI assistant to generate each file, guided by prompt templates. By the end, you will have a working app **and** understand why the code is split the way it is.

This project — `trip_notes/` — is the foundation you will keep building on through Labs 8–11, progressively adding AI features each week.

---

## What You Are Building

A command-line app to manage a personal travel wishlist:

```
=== Trip Notes ===
[1] Add destination
[2] View all destinations
[3] Search by country
[4] Add note to a destination
[5] Quit
```

Data is saved to a local JSON file so it persists between runs.

---

## Project Structure

```
trip_notes/
├── src/
│   ├── main.py       ← menu loop, user interaction
│   ├── models.py     ← Destination + TripCollection classes
│   └── storage.py    ← load/save JSON
├── data/
│   └── trips.json    ← auto-created when you add your first trip
├── tests/
│   └── test_flow.py  ← provided by instructor, do not modify
├── requirements.txt
└── README.md
```

Three source files. Two classes. One test file you don't write. This is the key idea of the lab.

---

## Prerequisites

- Lab 05 completed (you have a terminal AI tool set up: Gemini CLI or GitHub Copilot)
- Python 3.10+ installed
- Basic Python (functions, lists, dicts)

---

## Part 1 — In-Class Exercises (70 pts)

Work through these exercises with your instructor. Each exercise builds directly on the previous one.

**Choose your AI workflow — pick one and stick with it:**

| | Option A: Terminal AI | Option B: Copilot Chat Sidebar |
|---|---|---|
| **AI runs in** | Terminal 1 (Gemini CLI / Claude Code) | VS Code sidebar (Copilot Chat) |
| **Run/Test runs in** | Terminal 2 | The only terminal |
| **@file reference** | `@prompts/Lab07_Ex02_models.md` | `#file:trip_notes/prompts/Lab07_Ex02_models.md` |
| **Best for** | Full control, automation | Easy model switching, chat history |

*See the VS Code layout diagram from your instructor for the recommended screen setup.*

**Setting up terminals (see diagram):**
- **Option A:** Open two terminals side by side (`+` icon, then split with ⎘). Left = **AI Terminal** (Gemini / Claude Code), right = **Run Terminal** (run, test, git).
- **Option B:** Open one terminal (**Run Terminal**). Copilot Chat is in the sidebar (chat icon, or `Ctrl+Alt+I`).

**Where to work:** Exercise 1 runs from your `CISC395/` root. After that, your terminal(s) stay inside `trip_notes/` for the rest of the lab.

**Git:** CISC395 already has a git repository — do **not** run `git init`. `git` commands work from inside `trip_notes/` because git automatically finds the `.git` folder one level up. Your instructor will verify your progress through your CISC395 commit history.

---

### Exercise 1 — Create the Project Structure (10 pts)

**Step 1 — Make sure you are in your CISC395 workspace root** (Terminal 2):
```bash
# You should see CISC395/ — NOT Labs/ or Lab07/
pwd          # Mac/Linux
cd           # Windows (shows current path)
```

**Step 2 — Download and run the setup script:**

First, create the directory if it doesn't exist yet, then download `setup.py`:
```bash
# Mac/Linux/Windows
mkdir -p Labs/Lab07
curl -o Labs/Lab07/setup.py https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab07/setup.py
```

> **Windows (if curl doesn't work):** Use PowerShell instead:
> ```powershell
> New-Item -ItemType Directory -Force -Path Labs\Lab07
> Invoke-WebRequest -Uri https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab07/setup.py -OutFile Labs\Lab07\setup.py
> ```

Then run it:
```bash
python Labs/Lab07/setup.py
```

This creates `trip_notes/` inside your CISC395 folder and automatically downloads `tests/test_flow.py` and all `prompts/` files directly into it. You only need to do this once.

**Step 3 — Enter `trip_notes/`, then start your AI:**

```bash
cd trip_notes
```

- **Option A (Terminal AI):** run this in both terminals, then launch your AI in the AI Terminal (e.g., `gemini`). `@prompts/...` paths work from `trip_notes/`.
- **Option B (Copilot Chat):** run this in your Run Terminal. Copilot Chat sidebar uses `#file:trip_notes/prompts/...` paths from the workspace root — no `cd` needed for the sidebar itself.

Verify your structure (Run Terminal):
```bash
# Mac/Linux
find . -type f
# Windows
tree
```

**Step 4 — Run the test to confirm setup** (Run Terminal):
```bash
python tests/test_flow.py
# Expected: ImportError on all tests (normal — src/ files are still empty)
```

> **The test is your progress tracker.** Run `python tests/test_flow.py` after each exercise to see exactly where you are. Here is what you should see at each stage:
>
> ```
> After Ex 1 (src/ empty):     all sections FAIL (ImportError — expected)
> After Ex 2 (models.py done): Imports ✓  Destination ✓  TripCollection ✓  Storage ✗  Main ✗
> After Ex 3 (storage.py done):Imports ✓  Destination ✓  TripCollection ✓  Storage ✓  Main ✗
> After Ex 4 (main.py done):   Imports ✓  Destination ✓  TripCollection ✓  Storage ✓  Main ✓
> ```
>
> **After Ex4, all sections must show ✓ before you commit.**

**Deliverable:** Paste the output of the structure verification command (Step 3).

```
├───data
├───prompts
├───src
│   └───__pycache__
└───tests
```

**Understanding check (required):** In one sentence — why do we separate code into `src/`, `data/`, and a root level instead of putting everything in one folder?

```
[It allows us to seperate the structure and the alrady written data]
```

**Git commit** (use this exact message):
```bash
git add .
git commit -m "scaffold: project structure"
git push
```

> Use the commit messages exactly as shown. Your instructor checks commit history.

---

### Exercise 2 — Build `models.py` (20 pts)

This file defines what a "destination" looks like **and** how a collection of them behaves.

**Send this to your AI (one line):**

```
# Option A — Gemini CLI / Claude Code  (Terminal 1, from inside trip_notes/)
Please read and follow the instructions in @prompts/Lab07_Ex02_models.md

# Option B — Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab07_Ex02_models.md
```

The AI reads the prompt file and writes `src/models.py` directly.

**Understanding check (required):** You have two classes in one file — `Destination` and `TripCollection`. Describe their relationship in one sentence. Then: if a teammate wanted to add a `Hotel` booking feature to this app, would they add it to `models.py` or create a new file? Why?

```
[Your answer]
```

**Run the test to see your progress** (Run Terminal):
```bash
python tests/test_flow.py
# Imports, Destination, TripCollection sections should now pass
```
This shows which parts of the architecture are working. Notice that `storage` and `main` sections still fail — that is expected.

**Git commit** (use this exact message):
```bash
git add src/models.py
git commit -m "feat: Destination and TripCollection classes"
git push
```

---

### Exercise 3 — Build `storage.py` (15 pts)

This file handles reading and writing data. The rest of the app never touches JSON directly — it just calls these two functions.

**Send this to your AI (one line):**

```
# Option A — Gemini CLI / Claude Code  (AI Terminal, from inside trip_notes/)
Please read and follow the instructions in @prompts/Lab07_Ex03_storage.md

# Option B — Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab07_Ex03_storage.md
```

The AI reads `src/models.py` first, then writes `src/storage.py` directly.

**Understanding check (required):** Your team decides next semester to switch from saving to a JSON file to saving to a real database. Which files in this project would need to change? Which files would stay exactly the same, and why?

```
[i would change the src/storage file and replace the json logiv with database logic so it can be written better]
```

**Run the test to see your progress** (Run Terminal):
```bash
python tests/test_flow.py
# Imports, Destination, TripCollection, and Storage sections should now pass
```
You should see more sections passing than after Ex2. Only the `main` section will still fail.

**Git commit** (use this exact message):
```bash
git add src/storage.py
git commit -m "feat: JSON persistence"
git push
```

---

### Exercise 4 — Build `main.py` (25 pts)

This is the entry point — the menu loop the user interacts with.

**Send this to your AI (one line):**

```
# Option A — Gemini CLI / Claude Code  (AI Terminal, from inside trip_notes/)
Please read and follow the instructions in @prompts/Lab07_Ex04_main.md

# Option B — Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab07_Ex04_main.md
```

The AI reads `src/models.py` and `src/storage.py` first, then writes `src/main.py` directly.

**Test it** (Run Terminal):
```bash
python src/main.py
```
If you see `ModuleNotFoundError: No module named 'src'`, tell your AI: *"Fix the import error — ModuleNotFoundError: No module named 'src'."* It will add the path fix automatically.

**Understanding check (required):** Look at your three files. `main.py` imports from `models.py` and `storage.py`, but those two files don't import from `main.py`. In Lab 11, you will replace `main.py` with a Streamlit web app — which files will you be able to reuse without changing a single line? What does that tell you about how the project is designed?

```
[Your answer]
```

**Git commit** (use this exact message):
```bash
git add src/main.py
git commit -m "feat: CLI menu with 5 options"
git push
```

---

### Integration Test — Validate All Three Files

**Step 1 — Try running the app** (Run Terminal):
```bash
python src/main.py
```
If the menu appears with no errors, all three files are wired together correctly — proceed to Exercise 5.

**If you see an error**, fix it before continuing. Choose one approach:

**Option A — let the AI debug itself** (AI Terminal):
```
Run python src/main.py and fix any error you find. Do not modify tests/test_flow.py.
```
The AI runs the command, sees the error, and edits the files directly. Fast and hands-off, but uses more tokens.

**Option B — paste the error** (copy from Run Terminal → paste to AI):
Copy just the error message from the Run Terminal and paste it into your AI:
```
python src/main.py throws this error:
[paste the error message here]

Read src/models.py, src/storage.py, and src/main.py, identify the cause, and fix it.
```
More targeted — you control exactly what information the AI sees. Useful if you want to understand what went wrong.

After fixing, run the app again. Once the menu appears cleanly, commit any fixes:
```bash
git add src/models.py src/storage.py src/main.py
git commit -m "fix: pass integration tests"
git push
```

---

### Exercise 5 — Run and Test (10 pts)

Run the full app (`python src/main.py`) and complete all four steps:

1. **Add 3 destinations** — add places you want to visit or have visited (different countries)
2. **Add a note** to at least one destination using menu option [4]
3. **View all destinations** using menu option [2] — paste the full output below
4. **Search by country** using menu option [3] — paste one search result below

**Paste the output of "View all destinations" (option [2]):**

```
1. Joes Island (Joelandia) - $10000.00
2. New York City (USA) - $20.00
3. Your moms house (Earth) - $0.00
   Notes: ['huge to see from china']
```

**Paste the output of "Search by country" (option [3]):**

```
[New York City (USA) - $20.00]
```

**Step 5 — Open `data/trips.json` in VS Code Explorer:**

After adding trips, click on `data/trips.json` in the VS Code file tree (left panel). You will see the raw JSON that `storage.py` wrote to disk — every destination you entered is stored here as structured data. This file updates every time you add or change a destination. Your data persists between runs because `storage.py` reads from this file when the app starts.

> This is the persistence layer in action. The app never writes to disk directly from `main.py` — it always goes through `storage.py`, which is the only file that knows the file path and JSON format.

**Git commit** (use this exact message):
```bash
git add data/trips.json
git commit -m "test: add initial trip data"
git push
```

---

## Part 2 — Extend Your App (10 pts)

**This is homework.** Choose **one** of the three templates below and implement it, or propose your own feature with instructor approval.

Every template follows the same pattern:
- **`models.py`**: add a field to `Destination` and/or add methods to `TripCollection`
- **`main.py`**: add one or two new menu options that call those methods
- **`storage.py`**: no changes needed — `asdict()` handles new fields automatically

---

### Template A — Visited Tracker

Track which destinations you have visited vs. which are still on your wishlist.

**Changes to `models.py`:**
- Add `visited: bool = False` to `Destination`
- Add to `TripCollection`:
  - `get_wishlist() → list[Destination]` (visited == False)
  - `get_visited() → list[Destination]` (visited == True)
  - `mark_visited(index: int) → None` (sets `_trips[index].visited = True`)

**Changes to `main.py`:**
- Add `[6] Mark as Visited` — show list, user picks a trip, call `mark_visited()`
- Add `[7] Wishlist / Visited Stats` — show count of each and list them separately

**In Terminal 1, reference the prompt file:**

```
# Option A — Gemini CLI / Claude Code  (Terminal 1, from inside trip_notes/)
Please read and follow the instructions in @prompts/Lab07_P2A_visited.md

# Option B — Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab07_P2A_visited.md
```

---

### Template B — Trip Statistics

Add a statistics view that summarizes your saved trips.

**Changes to `models.py` — add to `TripCollection`:**
- `total_budget() → float` — sum of all trip budgets
- `average_budget() → float` — average budget (return 0.0 if empty)
- `top_country() → str` — the country appearing most often
- `count_by_country() → dict[str, int]` — counts per country

**Changes to `main.py`:**
- Add `[6] Show Statistics` — display all four stats in a formatted summary

**In Terminal 1, reference the prompt file:**

```
# Option A — Gemini CLI / Claude Code  (Terminal 1, from inside trip_notes/)
Please read and follow the instructions in @prompts/Lab07_P2B_stats.md

# Option B — Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab07_P2B_stats.md
```

---

### Template C — Trip Rating

Let users rate destinations and find their top-rated picks.

**Changes to `models.py`:**
- Add `rating: int = 0` to `Destination` (0 = unrated, 1–5 scale)
- Add to `TripCollection`:
  - `rate(index: int, rating: int) → None` (validates 1–5)
  - `top_rated(n: int = 3) → list[Destination]` — top n by rating
  - `get_by_min_rating(min_rating: int) → list[Destination]`

**Changes to `main.py`:**
- Add `[6] Rate a Trip` — show list, user picks a trip and enters 1–5
- Add `[7] View Top Rated` — display top 3 with their ratings

**In Terminal 1, reference the prompt file:**

```
# Option A — Gemini CLI / Claude Code  (Terminal 1, from inside trip_notes/)
Please read and follow the instructions in @prompts/Lab07_P2C_rating.md

# Option B — Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab07_P2C_rating.md
```

---

### Part 2 Deliverables

**Which template did you choose (or describe your custom feature):**

```
[Template A / B / C / Custom: ...]
```

**Terminal output showing the new feature working:**

```
[I did them all actually to see how expansive this app can get.]
```

**Git commit** — use format `feat: template-[A/B/C] [feature name]`:
```bash
git add src/models.py src/main.py
git commit -m "feat: template-A visited tracker"   # replace with your template + name
git push
```

---

## Part 3 — Design Your Own Mini App (20 pts)

**This is homework.** You will design a small structured Python project from scratch and write the prompt files an AI would need to build it.

You do **not** need to run or test the generated code. The deliverable is the design and the prompts — showing that you know what to ask for, not just how to execute someone else's plan.

---

### Step 1 — Choose an App (or Propose Your Own)

Pick one from the list below, or propose your own with instructor approval. Your app must have **three elements**: a data class, a collection class, and a menu interface.

| App | Data class | Collection (interesting operations) |
|-----|-----------|-------------------------------------|
| **Flashcard Deck** | `Card(front, back, difficulty)` | `Deck`: quiz mode, random draw, filter by difficulty |
| **Movie Watchlist** | `Movie(title, genre, rating, watched)` | `Watchlist`: unwatched list, top-rated, random pick |
| **Budget Tracker** | `Expense(amount, category, date)` | `Budget`: total by category, monthly summary, largest expense |
| **Habit Tracker** | `Habit(name, frequency, streak)` | `HabitLog`: check-in, streak count, today's completion rate |
| **Quote Collection** | `Quote(text, author, category)` | `QuoteBook`: random display, search by author, favorites |

**My app choice:**
```
[App name / Custom description]
```

---

### Step 2 — Design the Structure

Apply the two-question framework before writing any code.

**What does the app need to store?**
```
Data class name: ___________
Fields (name + type for each):
  -
  -
  -
```

**What does the app need to do?**
```
Collection class name: ___________
Methods (name + one-line description for each):
  -
  -
  -

Menu options:
  [1]
  [2]
  [3]
  [4] Quit
```

**Project folder and files:**
```
[your_app]/
├── src/
│   ├── models.py     ← data class + collection class
│   ├── storage.py    ← load/save JSON (same pattern as trip_notes)
│   └── main.py       ← menu loop
├── prompts/
│   ├── Lab07_P3_models.md   ← you write this
│   └── Lab07_P3_main.md     ← you write this
└── data/
```

---

### Step 3 — Write Your Prompt Files

Create a folder named after your app (e.g., `flashcard_deck/`) inside your CISC395 root, alongside `trip_notes/`. Inside it, create a `prompts/` folder and write **at least two prompt files**:

- **`Lab07_P3_models.md`** — instructs an AI to create `src/models.py` with your data class and collection class
- **`Lab07_P3_main.md`** — instructs the AI to read `src/models.py` first, then create `src/main.py` with your menu

**Scope guideline:** Keep it simple — 1 data class, 1 collection class, 3–4 menu options. If you chose a custom app, check with your instructor before writing prompts.

**Tips for writing effective prompts (from the patterns you saw in Part 1):**
- State the project structure at the top
- Tell the AI which existing files to read first
- Specify each class name, field, and method explicitly
- Say "Do not add an `if __name__ == '__main__'` block" for module files
- Say "Write the file directly to src/models.py" at the end

> **Using AI to review your draft prompts (recommended):**
> Before submitting, paste your prompt file into your AI and ask:
> ```
> Review this prompt file. Is it specific enough for an AI to generate correct Python code?
> What is missing or ambiguous? Suggest improvements.
> ```
> Revise based on the feedback. This is itself a vibe coding skill — using AI to sharpen your instructions before executing them.

**Paste your `Lab07_P3_models.md` content:**
````
[Paste your prompt file content here]
````

**Paste your `Lab07_P3_main.md` content:**
````
[Paste your prompt file content here]
````

**Git commit:**
```bash
git add [your_app]/
git commit -m "design: part3 [app name] prompts"
git push
```

---

### Step 4 — Reflection

**What was the hardest part of writing the prompt files?** What did you have to be more specific about than you expected? (3–4 sentences)

```
[Your answer]
```

**Compare your prompt files to the ones provided in Part 1** (look at `prompts/Lab07_Ex02_models.md`). What is one thing the Part 1 prompt does that you did not think to include? How might it affect the code the AI generates if that detail is missing? (2–3 sentences)

```
[Your answer]
```

---

## Submission

Submit **two things** on Blackboard:

1. **This `.md` file** with all understanding checks and terminal outputs filled in
2. **Your CISC395 GitHub repository URL** — your instructor will verify the commit history in `trip_notes/`

**Paste your GitHub repository URL here:**
```
https://github.com/[your-username]/CISC395
```

Expected commits (in order):
```
scaffold: project structure
feat: Destination and TripCollection classes
feat: JSON persistence
feat: CLI menu with 5 options
fix: pass integration tests          ← only if fixes were needed
test: add initial trip data
feat: template-[A/B/C] [feature name]
design: part3 [app name] prompts
```

Commit messages must match exactly (except the feature name portions). Missing or vague commit messages lose points.

---

## Grading Rubric

### Part 1 (70 pts)

| Exercise | Criteria | Points |
|----------|---------|--------|
| Ex 1: Structure | Correct directory layout + understanding check + commit | 10 |
| Ex 2: models.py | Both classes run correctly + understanding check + commit | 15 |
| Ex 3: storage.py | Test passes + understanding check + commit | 10 |
| Ex 4: main.py | All 5 menu options work + understanding check + commit | 25 |
| Ex 5: Run output | View all + search outputs pasted, data/trips.json committed | 10 |

### Part 2 (10 pts)

| Component | Criteria | Points |
|-----------|---------|--------|
| New feature works | New menu options run correctly (verified via commit) | 6 |
| Terminal output | Feature demonstrated in pasted output | 4 |

### Part 3 (20 pts)

| Component | Criteria | Points |
|-----------|---------|--------|
| Design table filled | Class names, fields, methods, menu options all specified | 5 |
| Prompt files written | At least 2 prompt files in repo, full content pasted in lab | 10 |
| Reflection | Both questions answered with substance | 5 |

**Understanding checks are required.** Empty answers lose those points.
**Commits are required.** Missing commits lose the commit portion of each exercise's points.

---

## Quick Reference

**All commands run from inside `trip_notes/`** (Run Terminal):
```bash
python src/main.py          # run the app
python tests/test_flow.py   # run integration tests
```
Check your location with `pwd` (Mac/Linux) or `cd` (Windows). If you see `CISC395/trip_notes` you are in the right place.

**Git workflow per exercise** (all from inside `trip_notes/`):
```bash
git add src/models.py       # or whichever file(s) changed
git commit -m "feat: ..."
git push
```

**Re-download tests and prompts** (if something went wrong):
```bash
cd ..                                   # go back to CISC395/ root
python Labs/Lab07/setup.py --refresh
cd trip_notes                           # return to working directory
```

**How to give a prompt file to your AI:**
```
# Option A — Gemini CLI / Claude Code  (AI Terminal, from inside trip_notes/)
Please read and follow the instructions in @prompts/Lab07_Ex02_models.md

# Option B — Copilot Chat sidebar  (workspace root = CISC395/)
Please read and follow the instructions in #file:trip_notes/prompts/Lab07_Ex02_models.md
```
Replace `Lab07_Ex02_models.md` with whichever file you need.

**Project grows in future labs:**
- Lab 08: Add an AI assistant that can answer questions about your trips
- Lab 09: Upload destination guides — AI searches them to give better advice
- Lab 10: Add tools (budget calculator, packing suggestions)
- Lab 11: Replace the CLI with a Streamlit web interface
