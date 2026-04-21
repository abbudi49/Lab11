# Lab 08: Adding AI to Trip Notes — API Programming Foundations

**Course:** CISC 395 Applied Generative AI and LLM Applications
**Week:** 9
**Points:** 100

---

## Overview

In Lab 07 you built a working CLI app entirely offline. This week you add the first AI feature: a travel assistant powered by a real language model.

**What changes in `trip_notes/` this week:**

```
trip_notes/
├── src/
│   ├── ai_assistant.py  ← NEW: API client + ask() function
│   ├── main.py          ← polish menu (Q key + grouping), add [6] Ask AI, [7] Briefing
│   ├── models.py        (unchanged)
│   └── storage.py       (unchanged)
├── .env                 ← NEW: your API key (never commit this)
├── .gitignore           ← NEW: protects .env and .venv
├── requirements.txt     ← updated: openai, python-dotenv
└── ...
```

**AI tool:** Use Gemini CLI, GitHub Copilot, Claude Code, or any terminal AI. All exercises use `@prompts/` files — no copy-paste needed.

---

## Setup

Run from your **CISC395 root** to download prompt files and the test file:

```bash
mkdir -p Labs/Lab08
curl -o Labs/Lab08/setup.py https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab08/setup.py
python Labs/Lab08/setup.py
```

> **Windows (if curl doesn't work):** Use PowerShell:
> ```powershell
> New-Item -ItemType Directory -Force -Path Labs\Lab08
> Invoke-WebRequest -Uri https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab08/setup.py -OutFile Labs\Lab08\setup.py
> ```

Steps 1–4 run from **CISC395/ root**. Steps 5–6 run from **`trip_notes/`**.

**Step 1 — Create `CISC395/.gitignore`** (manually in VS Code or any text editor):
```
.env
.venv/
__pycache__/
*.pyc
chroma_db/
```
Then commit and push **before creating `.env`**:
```bash
git add .gitignore
git commit -m "chore: add gitignore"
git push
```
> If `.env` enters git history before `.gitignore` is committed, your API key is permanently recorded — even if you delete the file later.

**Step 2 — Create `CISC395/.env`** (never commit this file):
```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```
Get a free key at openrouter.ai (no credit card required). Gemini alternative: `GEMINI_API_KEY=AIza-...` from aistudio.google.com.

**Step 3 — Create `.venv` (skip if already exists from a previous lab):**
```bash
python -m venv .venv
```
Or in VS Code: `Ctrl+Shift+P` → *Python: Create Virtual Environment* → select `.venv`.

Activate and install:
```bash
# Activate — Windows:
.venv\Scripts\activate
# Activate — Mac/Linux:
source .venv/bin/activate

pip install openai python-dotenv
pip freeze > requirements.txt
```
> `.venv/` and `.env` both live at `CISC395/` root and are shared across all labs. VS Code auto-detects `.venv` since it is at the workspace root.

> **Windows PowerShell error?** Run once: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Step 4 — Enter `trip_notes/` in both terminals:**
```bash
cd trip_notes
```
**AI (Option A):** launch Gemini CLI (`gemini`) or Claude Code. **Run Terminal:** all python, git, and test commands. `.venv` stays active after `cd`.

**Step 5 — Run the setup check (Run Terminal):**
```bash
python tests/check_api_setup.py
```
Checks `CISC395/.gitignore`, `.env`, `.venv`, `requirements.txt`, then automatically tests your API key. **Fix every failure before continuing.**

If OpenRouter is unavailable, try the Gemini backup:
```bash
python tests/check_gemini.py
```
The script prints the exact lines to swap into `ai_assistant.py`.

**Step 6 — Run the code structure check (Run Terminal):**
```bash
python tests/test_ai_assistant.py
# Expected: import error — src/ai_assistant.py is empty (normal for now)
```

**Step 7 — Polish the menu before adding AI options:**

**AI (one line):**
```
# Option A — Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab08_Setup_menu.md

# Option B — Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab08_Setup_menu.md
```

This refactors `main.py` to use `[Q]` to quit and adds visual grouping with an empty `-- AI --` section ready for Ex 3. Verify it works:
```bash
python src/main.py
# Menu should show grouped sections and Q to quit
```

Then commit:
```bash
git add src/main.py ../requirements.txt
git commit -m "chore: lab08 environment ready"
git push
```

---

## Exercises

### Exercise 1 — Build `src/ai_assistant.py` (25 pts)

This file holds the API client, the `ask()` function, and the system prompt. All AI logic lives here so `main.py` stays focused on the menu.

**AI (one line):**
```
# Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab08_Ex01_assistant.md

# Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab08_Ex01_assistant.md
```

The AI reads the prompt file and writes `src/ai_assistant.py` directly.

**Verify structure (Run Terminal):**
```bash
python tests/test_ai_assistant.py
# ask(), TRAVEL_SYSTEM_PROMPT, client, MODEL should all pass
```

**Live API test (Run Terminal):**
```bash
python src/ai_assistant.py
```

**Paste the output of `python src/ai_assistant.py`:**

```
[Paste AI response here]
```

**Understanding check (required):** `TRAVEL_SYSTEM_PROMPT` is defined in `ai_assistant.py`, not in `main.py`. Using the separation of concerns idea from Lab 07 — which layer does `ai_assistant.py` represent? What would break if you moved the system prompt into `main.py`?

```
[Your answer]
```

**Git commit:**
```bash
git add src/ai_assistant.py requirements.txt
git commit -m "feat: ai_assistant.py with ask() function"
git push
```

---

### Exercise 2 — Temperature and System Prompt (25 pts)

#### Part A — Temperature experiment (15 pts)

Ask the same travel question at three temperatures. Run each **twice** using a short script in the Run Terminal:

```python
# Run from trip_notes/ — save as temp_test.py or paste directly into python shell
from src.ai_assistant import ask, TRAVEL_SYSTEM_PROMPT
print(ask("Suggest a unique activity for a solo traveler visiting Tokyo.",
          system_prompt=TRAVEL_SYSTEM_PROMPT,
          temperature=0.1))
```

Change `temperature=` to `0.1`, `0.7`, and `1.4` for each row. Run each twice.

Suggested question: `"Suggest a unique activity for a solo traveler visiting Tokyo."`

| Temperature | Run 1 (first 15 words) | Run 2 (first 15 words) |
|-------------|----------------------|----------------------|
| 0.1 | | |
| 0.7 | | |
| 1.4 | | |

**Analysis:** What pattern do you see across the three temperatures? For a feature that recommends well-known landmarks, which temperature would you choose? For generating creative trip ideas, which one? (3–4 sentences)

```
[Your analysis]
```

#### Part B — System prompt in action (10 pts)

Test `TRAVEL_SYSTEM_PROMPT` with these two messages:

Message 1: `"I have $500 and 5 days. Where should I go in Southeast Asia?"`
Message 2: `"Is it safe to travel alone as a student?"`

**Output from Message 1:**
```
[Paste here]
```

**Output from Message 2:**
```
[Paste here]
```

**Reflection:** Pick one response and identify a specific phrase that shows the persona is working. If the persona is not visible, rewrite the system prompt and test again. (2–3 sentences)

```
[Your reflection]
```

---

### Exercise 3 — Add AI to the Menu (20 pts)

Add option `[6] Ask AI` to `main.py` so users can ask travel questions and optionally save the answer as a note on a saved trip.

**AI (one line):**
```
# Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab08_Ex03_menu.md

# Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab08_Ex03_menu.md
```

**Test the full app (Run Terminal):**
```bash
python src/main.py
```

**Paste a test session showing:**
1. Asking the AI a travel question via option [6]
2. Saving the AI response as a note on a saved trip
3. Viewing that trip (option [2]) to confirm the note was attached

```
[Paste terminal output here]
```

**Understanding check (required):** `main.py` calls `ask()` from `ai_assistant.py` — it doesn't know what model is running or how errors are handled. Following the same dependency rule as Lab 07, what would you need to change to switch from LLaMA to a different model? Which files would you touch?

```
[Your answer]
```

**Git commit:**
```bash
git add src/main.py
git commit -m "feat: Ask AI menu option"
git push
```

---

### Exercise 4 — Prompt Chaining: Trip Briefing (20 pts)

Build a two-step AI pipeline where the output of Call 1 becomes the input of Call 2. Then connect it to your saved trips data.

#### Part A — Build `generate_trip_briefing()` (10 pts)

**AI (one line):**
```
# Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab08_Ex04_chaining.md

# Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab08_Ex04_chaining.md
```

**Run the structure test (Run Terminal):**
```bash
python tests/test_ai_assistant.py
# generate_trip_briefing() section should now pass (city, country, notes)
```

**Run the live test (Run Terminal):**
```bash
python src/ai_assistant.py
```

**Paste the output for `generate_trip_briefing("Tokyo", "Japan")`:**

```
Overview:
[paste]

Packing list:
[paste]
```

**Understanding check (required):** The packing list (Call 2) uses the overview text from Call 1 as its input, not just the city name. Why does giving Call 2 more context produce a better packing list? What would the packing list look like if Call 2 only received `"Tokyo"`? (2–3 sentences)

```
[Your answer]
```

**Git commit:**
```bash
git add src/ai_assistant.py
git commit -m "feat: trip briefing prompt chain"
git push
```

---

#### Part B — Connect to Menu [7] (10 pts)

Now connect `generate_trip_briefing()` to your real saved trips. Option [7] reads destinations from `storage.py` and generates a personalized briefing using the trip's saved notes.

**AI (one line):**
```
# Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab08_Ex04b_menu.md

# Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab08_Ex04b_menu.md
```

**Add at least 2 destinations with notes (Run Terminal):**
```bash
python src/main.py
# Use option [1] to add trips, option [4] to add notes
# Then use option [7] to generate a briefing
```

> If a destination has no notes, the briefing still works — the `notes` parameter is optional and ignored when empty.

**Paste a test session showing:**
1. Selecting a destination from the numbered list
2. The generated Overview and Packing List output

```
[Paste terminal output here]
```

**Understanding check (required):** If one of your notes says "business conference" or "travelling with kids", does the briefing reflect it? Why does passing `dest.notes` into `generate_trip_briefing()` allow the AI to personalize the output? (2–3 sentences)

```
[Your answer]
```

**Git commit:**
```bash
git add src/main.py
git commit -m "feat: trip briefing menu option"
git push
```

---

### Reflection (10 pts)

**1.** What is `.venv/` and why do we create it? What would happen if two different projects on your computer used the same global Python environment instead of separate `.venv/` folders?

```
[2–3 sentences]
```

**2.** What does `pip install openai python-dotenv` actually do? Why do we also run `pip freeze > requirements.txt` afterward — what problem does that file solve?

```
[2–3 sentences]
```

**3.** You committed `.gitignore` before creating `.env`. Why does the order matter? What would happen if you created `.env` first, committed it, then added it to `.gitignore`?

```
[2–3 sentences]
```

**4.** In this lab, every time a user types a travel question, your app makes an API call to OpenRouter. What is actually happening in that call — what does your app send, and what does it get back? How is this different from just searching Google?

```
[3–4 sentences]
```

---

## Grading Rubric

| Exercise | Criteria | Points |
|----------|---------|--------|
| Ex 1: ai_assistant.py | Structural test passes, live API output pasted, understanding check answered | 25 |
| Ex 2A: Temperature | Table filled with real outputs, analysis addresses pattern | 15 |
| Ex 2B: System prompt | Two outputs pasted, reflection identifies specific phrase | 10 |
| Ex 3: Menu option | App runs, test session pasted (ask + save + view), understanding check answered | 20 |
| Ex 4A: Prompt chaining | Structural test passes (city/country/notes), output pasted, understanding check answered | 10 |
| Ex 4B: Menu integration | Option [7] runs with real data, test session pasted, understanding check answered | 10 |
| Reflection | Both questions answered with substance | 10 |

**Understanding checks are required.** Empty answers lose those points.
**Commits are required.** Missing commits lose the commit portion of each exercise's points.

---

## Quick Reference

**Always run from inside `trip_notes/`** (with `.venv` active in Run Terminal):
```bash
python src/main.py          # run the full app
python src/ai_assistant.py  # test API directly
python tests/test_ai_assistant.py    # structural checks
```

**Activate venv** (if you opened a new terminal):
```bash
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate
```

**Re-download prompts and test file** (from CISC395/ root):
```bash
cd ..
python Labs/Lab08/setup.py --refresh
cd trip_notes
```

**messages structure:**
```python
messages = [
    {"role": "system", "content": "You are a travel assistant."},
    {"role": "user",   "content": "What should I pack for Iceland?"},
]
```

**Model and extra_body:**
```python
MODEL = "openrouter/free"
# Always include extra_body — required for openrouter/free routing
extra_body = {"reasoning": {"enabled": True}}
```
`openrouter/free` routes to the best available free model. With reasoning enabled, `content` may be `None` — the `ask()` function handles this automatically.

**Next lab:** Lab 09 adds RAG — upload your own destination guide documents and let the AI search them before answering.
