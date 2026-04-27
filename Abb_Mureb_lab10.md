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
[import json
    2 import requests
    3 import sys
    4 import os
    5
    6 # Allow importing from the same directory if run as a script
    7 sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    8
    9 from src.rag import search_guides
   10
   11 def budget_breakdown(total_budget: float, duration_days: int) -> str:
   12     """Splits a total budget into daily averages and categories."""
   13     if duration_days <= 0:
   14         return "Duration must be at least 1 day."
   15
   16     daily_avg = total_budget / duration_days
   17     accommodation = total_budget * 0.40
   18     food = total_budget * 0.30
   19     activities = total_budget * 0.20
   20     emergency = total_budget * 0.10
   21
   22     return (
   23         f"--- BUDGET BREAKDOWN (${total_budget:,.2f} over {duration_days} days) ---\n"
   24         f"Daily Average: ${daily_avg:,.2f}/day\n\n"
   25         f"Categories:\n"
   26         f"- Accommodation (40%): ${accommodation:,.2f}\n"
   27         f"- Food & Dining (30%): ${food:,.2f}\n"
   28         f"- Activities (20%): ${activities:,.2f}\n"
   29         f"- Emergency/Misc (10%): ${emergency:,.2f}"
   30     )
   31
   32 def get_weather(city: str) -> str:
   33     """Fetches the current real-time weather for a city using wttr.in."""
   34     try:
   35         response = requests.get(f"https://wttr.in/{city}?format=3", timeout=10)
   36         if response.status_code == 200:
   37             return f"Current weather in {response.text.strip()}"
   38         return f"Could not retrieve weather for {city} (Status: {response.status_code})"
   39     except Exception as e:
   40         return f"Error fetching weather: {str(e)}"
   41
   42 def search_guides_tool(query: str) -> str:
   43     """Searches local travel guides for information."""
   44     results = search_guides(query, n_results=3)
   45     if not results:
   46         return f"No information found in local guides for: {query}"
   47     combined_results = "\n\n---\n\n".join(results)
   48     return f"Information found in guides:\n\n{combined_results}"]
```

**Paste the test output:**
```
[Testing budget_breakdown:                                                                                                       │    
│ --- BUDGET BREAKDOWN ($1,000.00 over 5 days) ---                                                                                │    
│ Daily Average: $200.00/day                                                                                                      │    
│                                                                                                                                 │    
│ Categories:                                                                                                                     │    
│ - Accommodation (40%): $400.00                                                                                                  │    
│ - Food & Dining (30%): $300.00                                                                                                  │    
│ - Activities (20%): $200.00                                                                                                     │    
│ - Emergency/Misc (10%): $100.00                                                                                                 │    
│                                                                                                                                 │    
│ Testing get_weather (Tokyo):                                                                                                    │    
│ Current weather in tokyo: ⛅  +64°F                                                                                             │    
│                                                                                                                                 │    
│ Testing search_guides_tool (Paris):                                                                                             │    
│ Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster  │    
│ downloads.                                                                                                                      │    
│ Loading weights: 100%|████████████████████████████████████████████████████████████████████| 103/103 [00:00<00:00, 3877.34it/s]  │    
│ BertModel LOAD REPORT from: sentence-transformers/all-MiniLM-L6-v2                                                              │    
│ Key                     | Status     |  |                                                                                       │    
│ ------------------------+------------+--+-                                                                                      │    
│ embeddings.position_ids | UNEXPECTED |  |                                                                                       │    
│                                                                                                                                 │    
│ Notes:                                                                                                                          │    
│ - UNEXPECTED:   can be ignored when loading from different task/architecture; not ok if you expect identical arch.              │    
│ Information found in guides:                                                                                                    │    
│                                                                                                                                 │    
│ © PromptGuides.com 5-day Paris City Guide 31© PromptGuides.com Photo credits Cover page Cover photo #1: Photo by CpaKmoi Cover  │    
│ photo #2: Photo by Paolo Margari Cover photo #3: Photo by cisko Map http://www.bing.com/maps Attraction details Trocadéro Garde │    
│ ns: Photo by Angel T. • Eiffel Tower: Photo by BurgTender • Parc du Champ de Mars: Photo by Steve B Chamberlain • Musée Rodin:  │    
│ Photo by cisko • Army Museum and Tomb of Napoleon : Photo by Giorgos Michalogiorgakis • Hotel des Invalides: Photo by feliven • │    
│  Grand and Petit Palais: Photo by HarshLight • Champs-Elysées: Photo by wallyg • Arc de Triomphe: Photo by Rik_C • Musée du Lou │    
│ vre: Photo by Dimitry B • Tuileries Garden: Photo by levork • Musée de l'Orangerie: Photo by fmpgoh • Centre Georges Pompidou:  │    
│ Photo by wallyg • Hotel de Ville: Photo by Storm Crypt • La Madeleine: Photo by teachandlearn • Opéra Garnier: Photo by Istvan  │    
│ • Galeries Lafayette: Photo by Ghislain Sillaume • Notre Dame Cathedral: Photo by Amol Hatwar • Tower of Notre Dame Cathedral:  │    
│ Photo by Chirag D. Shah • Sainte-Chapelle: Photo by IceNineJon • La Conciergerie: Photo by bibi0328 • Luxembourg Gardens: Photo │    
│  by Kewei SHANG • The Panthéon: Photo by                                                                                        │    
│                                                                                                                                 │    
│ ---                                                                                                                             │    
│                                                                                                                                 │    
│ for savory galettes (buckwheat crêpes with ham, egg, and cheese) for a real meal - **Wine and cheese picnic** — buy from a from │    
│ agerie and a cave à vins, then eat in the Champ de Mars or Luxembourg Gardens ## Activities - **Musée d'Orsay** houses the worl │    
│ d's best Impressionist collection (Monet, Renoir, Degas) — less crowded than the Louvre and free on the first Sunday of each mo │    
│ nth - **Walk along the Seine** from Notre-Dame to the Eiffel Tower — about 4km, passing Shakespeare and Company bookstore - **M │    
│ ontmartre neighborhood** — Sacré-Cœur basilica at the top has a panoramic view; the surrounding streets have artists and cafés  │    
│ - **Versailles** day trip (45 min by RER C train) — arrive before 10am to beat tour groups ## Practical Tips A **Carnet** (book │    
│  of 10 Métro tickets) is cheaper than buying single tickets. Tipping is not required but rounding up the bill is appreciated. M │    
│ any Paris museums are free for visitors under 26 from EU countries — check eligibility before paying. Most restaurants do not o │    
│ pen for dinner before 7pm. ## Budget Paris is moderately expensive. Mid-range budget: €120–€180 per day including a 3-star hote │    
│ l, two sit-down meals, and admissions. Picnic lunches                                                                           │    
│                                                                                                                                 │    
│ ---                                                                                                                             │    
│                                                                                                                                 │    
│ 17:30-18:15 La Défense THINGS YOU NEED TO KNOW La Défense is Paris' financial district with skyscrapers 14 out of the 72 glass  │    
│ and steel buildings are higher than 150 meters It was purposely built to the west of the city to keep the centre free of skyscr │    
│ apers La Défense is Europe's largest purpose-built business district More than 150.000 people work here Paris' Historical Axis  │    
│ ends here, a 10 km long imaginary line that connects the city's main historical sites (Louvre, Champs-Élysées, Arc de Triomphe, │    
│  Grande Arche) Grande Arche is 100 meter tall and large enough to hold Notre-Dame in the middle THINGS TO DO THERE Leave the me │    
│ tro station and head to the Grande Arche Have a look at the surrounding skyscrapers Enjoy the view from the steps of the Grande │    
│  Arche. You can see the all the way down the Champs Elysees past the Arc de Triomphe and to the Louvre TIPS & INSIGHTS Lots of  │    
│ shopping possibilities around MORE Info and Photos > 5-day Paris City Guide 30 © PromptGuides.com 5-day Paris City Guide 31© Pr │    
│ omptGuides.com Photo credits Cover page Cover photo #1: Photo by CpaKmoi Cover photo #2: Photo by Paolo Margari Cover photo #3: │    
│  Photo by ]
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
[1  What is the weather in Paris?
   2 Thinking...
   3 [Tool call] get_weather({'city': 'Paris'})
   4 [Tool result] Current weather in paris: ☀️   +65°F
   5
   6 Final Answer:
   7 The current weather in Paris is sunny ☀️ with a temperature of about 65°F (≈18°C)
```

**Step 2 — Test with 3 questions:**

Run `python tests/test_agent.py` again for each question below. Copy-paste the question at the prompt:

Test 1 (computation): `I have $1200 for 8 days in Tokyo. Break down my budget.`
```
[ [Tool call] budget_breakdown({'total_budget': 1200, 'duration_days': 8})
    7 [Tool result] --- BUDGET BREAKDOWN ($1,200.00 over 8 days) ---
    8 Daily Average: $150.00/day
    9
   10 Categories:
   11 - Accommodation (40%): $480.00
   12 - Food & Dining (30%): $360.00
   13 - Activities (20%): $240.00
   14 - Emergency/Misc (10%): $120.00
   15
   16 Final Answer:
   17 Based on your $1,200 budget for 8 days in Tokyo, here is a suggested breakdown (approximately **$150 per day**):
   18
   19 - **Accommodation (40%): $480** ($60/night) — Look for business hotels, hostels, or capsule hotels in areas like Asakusa or Ueno.
   20 - **Food & Dining (30%): $360** ($45/day) — Enjoy great ramen, convenience store meals, and affordable izakayas.
   21 - **Activities (20%): $240** — Covers entry to shrines, a few museums, and local transportation (like a Suica card).
   22 - **Emergency/Misc (10%): $120** — Keep this for souvenirs or unexpected costs.
   23
   24 Tokyo is very manageable on this budget if you balance nicer meals with affordable street food!
]
```

Test 2 (real-time data): `What's the weather like in Paris right now?`
```
[[Tool call] get_weather({'city': 'Paris'})
    7 [Tool result] Current weather in paris: ☀️   +65°F
    8
    9 Final Answer:
   10 The current weather in Paris is sunny ☀️ with a temperature of about 65°F (≈18°C).
```

Test 3 (two tools): `I'm planning a trip to Tokyo. Check the current weather and search my travel guides for things to do.`
```
[Tool call] get_weather({'city': 'Tokyo'})
    7 [Tool result] Current weather in tokyo: ⛅  +64°F
    8 [Tool call] search_guides_tool({'query': 'things to do in Tokyo'})
    9 [Tool result] Information found in guides:
   10 ... Explore world-class dining, from sushi and ramen to regional specialties.
   11 ... Visit iconic sights: Meiji Shrine, Senso-ji Temple, Tokyo Skytree, Tokyo Tower.
   12 ... Stroll through historic districts (Asakusa) and modern neighborhoods (Shibuya, Shinjuku).
   13
   14 Final Answer:
   15 Here’s what I found for your Tokyo trip:
   16
   17 **Current Weather:**
   18 - 🌤️ 64°F (partly cloudy and mild).
   19
   20 **Things to Do (from your guides):**
   21 - **Sights:** Visit the Meiji Shrine, Senso-ji Temple, and the Tokyo Skytree for great views.
   22 - **Neighborhoods:** Explore the traditional streets of Asakusa or the modern energy of Shibuya and Shinjuku.
   23 - **Food:** Don't miss the world-class dining, especially the local ramen and sushi.
   24
   25 Enjoy planning your trip!
]
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
[
    1         elif choice == "10":
    2             try:
    3                 from src.tools import run_agent
    4             except Exception as e:
    5                 print(f"Agent support not available: {e}")
    6                 continue
    7             q = input("Enter question for the AI Travel Agent: ")
    8             print("\nThinking...")
    9             ans = run_agent(q)
   10             print("\n=== Agent Response ===")
   11             print(ans)]
```

**Paste a test session with one compound question:**
```
[hat is the current weather in Tokyo and what are some things to do there according to my
      guides?
    
   17 The current weather in Tokyo is ⛅ +64°F.
   18
   19 Top activities from your guides:
   20 1. **Explore Local Dining:** Try world-class sushi, ramen, and seasonal sweets.
   21 2. **Iconic Sights:** Visit the Meiji Shrine, Senso-ji Temple, and the Tokyo Skytree.
   22 3. **Neighborhood Walks:** Stroll through historic Asakusa or the vibrant Shibuya crossing.
   23 4. **Day Trips:** Consider visiting Nikko or Hakone for beautiful temples and mountain views.
   24
   25 Let me know if you'd like a budget breakdown for your Tokyo trip! 😊]
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
