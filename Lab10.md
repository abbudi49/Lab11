# Lab 10: Adding Tools to Trip Notes — Function Calling + ReAct Agent

**Course:** CISC 395 Applied Generative AI and LLM Applications
**Week:** 11
**Points:** 100

---

## Overview

Your AI assistant can now chat and search documents. This week you give it **tools**: Python functions the AI can call when it needs to compute something or take an action. You will build a ReAct agent — the AI reasons about which tool to use, calls it, and reasons again until it can give a final answer.

**What changes in `trip_notes/` this week:**

```
trip_notes/
├── src/
│   ├── tools.py        ← NEW: 3 travel tools + run_agent()
│   ├── main.py         ← add option [10] AI Travel Agent
│   ├── rag.py          (unchanged — search_guides_tool calls it)
│   ├── ai_assistant.py (unchanged)
│   ├── models.py       (unchanged)
│   └── storage.py      (unchanged)
├── guides/
├── chroma_db/
└── requirements.txt    (no new packages needed)
```

**Three tool types you will build:**

| Tool | Type | What it does |
|------|------|--------------|
| `budget_breakdown` | Pure computation | Math — splits budget by category |
| `get_weather` | External HTTP API | Fetches real-time weather (no API key needed) |
| `search_guides_tool` | Internal system call | Searches your guides/ via rag.py |

---

## Setup

**From CISC395/ root (one line):**

```bash
mkdir -p Labs/Lab10 && curl -o Labs/Lab10/setup.py https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab10/setup.py && python Labs/Lab10/setup.py
```

> **Windows PowerShell:**
> ```powershell
> New-Item -ItemType Directory -Force -Path Labs\Lab10; Invoke-WebRequest -Uri https://raw.githubusercontent.com/tisage/CISC395/refs/heads/main/Lab10/setup.py -OutFile Labs\Lab10\setup.py; python Labs\Lab10\setup.py
> ```

Then from **`trip_notes/`:**

```bash
cd trip_notes
python tests/check_progress.py --lab 10
```

Fix any red items before starting exercises.

---

## Exercises

---

### Exercise 1 — Build the Tools (30 pts)

Create `src/tools.py` with three travel tool functions that represent different tool types.

**AI (one line):**
```
# Option A — Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab10_Ex01_tools.md

# Option B — Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab10_Ex01_tools.md
```

**Run Terminal — test:**
```bash
python src/tools.py
```

**Paste your `src/tools.py`:**
```python
[Your code here]
```

**Paste the test output:**
```
[Paste here]
```

**Understanding check:** The three tools use three different approaches: pure math, an external HTTP API, and calling your own project's rag.py. What does this tell you about what a "tool" can be? Why is it better to separate these operations from the LLM instead of just asking the LLM directly? (3 sentences)

```
[Your answer]
```

**Commit:**
```bash
git add src/tools.py
git commit -m "feat: travel tools (budget, weather, guides search)"
git push
```

---

### Exercise 2 — Build the ReAct Agent (35 pts)

Add `run_agent()` to `src/tools.py`. The agent reasons about which tool to use, calls it, sees the result, and continues until it can give a final answer.

**AI (one line):**
```
# Option A — Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab10_Ex02_agent.md

# Option B — Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab10_Ex02_agent.md
```

**Step 1 — Quick test (Run Terminal):**

```bash
python tests/test_agent.py
```

Type or paste a question when prompted. You should see `[Tool call]` and `[Tool result]` lines before the final answer — this confirms the ReAct loop is working.

```
[Paste output here]
```

**Step 2 — Test with 3 questions:**

Run `python tests/test_agent.py` again for each question below. Copy-paste the question at the prompt:

Test 1 (computation): `I have $1200 for 8 days in Tokyo. Break down my budget.`
```
[Paste full output — should show [Tool call] budget_breakdown(...)]
```

Test 2 (real-time data): `What's the weather like in Paris right now?`
```
[Paste full output — should show [Tool call] get_weather(...)]
```

Test 3 (two tools): `I'm planning a trip to Tokyo. Check the current weather and search my travel guides for things to do.`
```
[Paste full output — should show two [Tool call] lines]
```

**Understanding check:** In Test 3, the agent called two different tool types (HTTP API + local guide search). Why couldn't the LLM answer both parts of that question without tools? (2–3 sentences)

```
[Your answer]
```

**Commit:**
```bash
git add src/tools.py tests/test_agent.py
git commit -m "feat: react agent with tool calling"
git push
```

---

### Exercise 3 — Add Agent to the Menu (20 pts)

Add menu option `[10] AI Travel Agent` to `main.py`.

**AI (one line):**
```
# Option A — Gemini CLI / Claude Code
Please read and follow the instructions in @prompts/Lab10_Ex03_menu.md

# Option B — Copilot Chat sidebar
Please read and follow the instructions in #file:trip_notes/prompts/Lab10_Ex03_menu.md
```

**Paste the `[10]` handler from `main.py`:**
```python
[Paste here]
```

**Paste a test session with one compound question:**
```
[Paste terminal output]
```

**Commit:**
```bash
git add src/main.py
git commit -m "feat: add agent to menu [10]"
git push
```

---

### Reflection (15 pts)

**1.** Compare options `[6]`, `[8]`, and `[10]` in your menu. For each, describe a travel question where it is the **best** choice and explain why. (6–8 sentences total)

```
[6] Ask AI:           best for...

[8] Search my guides: best for...

[10] AI Travel Agent: best for...
```

**2.** The `get_weather` tool calls a real external API. Why is it better to have the agent call this tool rather than just asking the LLM "what's the weather in Tokyo?" directly? What category of problem does this solve? (3 sentences)

```
[Your answer]
```

---

## Grading Rubric

| Exercise | Criteria | Points |
|----------|---------|--------|
| Ex 1: tools.py | All 3 functions work (budget, weather, guides search), TOOL_DEFINITIONS defined, output pasted | 30 |
| Ex 2: run_agent() | Agent loop works, 3 test outputs pasted incl. two-tool question | 35 |
| Ex 3: Menu [10] | Works in app, test session pasted, commit present | 20 |
| Reflection | Both questions answered with substance | 15 |

---

## Quick Reference

**OpenAI tool calling format:**

```python
response = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=TOOL_DEFINITIONS,
    tool_choice="auto",
    max_tokens=1024,
    timeout=30,
)
msg = response.choices[0].message

if msg.tool_calls:
    for tc in msg.tool_calls:
        name = tc.function.name
        args = json.loads(tc.function.arguments)
        result = your_function(**args)
        messages.append({"role": "assistant", "content": None, "tool_calls": [tc]})
        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
```

**Tool definition format:**

```python
# Example: a tool that calls an external API
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current real-time weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name"},
            },
            "required": ["city"],
        },
    },
}
```

The LLM reads the `description` field to decide when to call each tool. Write clear descriptions.

**Next lab:** Lab 11 replaces the CLI menu with a Streamlit web interface. All the code from Labs 07–10 will be reused — you are just changing how users interact with it.
