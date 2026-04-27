import json
import requests
import sys
import os

# Allow importing from src if run as a script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.rag import search_guides
except ImportError:
    # Fallback if src.rag is not in the path
    def search_guides(query, n_results=3):
        return []

def budget_breakdown(city: str, duration_days: int, total_budget: float) -> str:
    """
    Splits a total budget into daily averages and categories.
    
    Args:
        city (str): The destination city.
        duration_days (int): Number of days for the trip.
        total_budget (float): Total trip budget in USD.
        
    Returns:
        str: A formatted string showing the budget breakdown.
    """
    if duration_days <= 0:
        return "Duration must be at least 1 day."
    
    daily_avg = total_budget / duration_days
    
    # Simple percentage breakdown
    accommodation = total_budget * 0.40
    food = total_budget * 0.30
    activities = total_budget * 0.20
    emergency = total_budget * 0.10
    
    breakdown = (
        f"--- BUDGET BREAKDOWN for {city} (${total_budget:,.2f} over {duration_days} days) ---\n"
        f"Daily Average: ${daily_avg:,.2f}/day\n\n"
        f"Categories:\n"
        f"- Accommodation (40%): ${accommodation:,.2f}\n"
        f"- Food & Dining (30%): ${food:,.2f}\n"
        f"- Activities (20%): ${activities:,.2f}\n"
        f"- Emergency/Misc (10%): ${emergency:,.2f}"
    )
    return breakdown

def get_weather(city: str) -> str:
    """
    Fetches the current real-time weather for a city using wttr.in.
    
    Args:
        city (str): The name of the city.
        
    Returns:
        str: A brief weather summary.
    """
    try:
        # Use wttr.in with ?format=3 for a concise one-line summary
        response = requests.get(f"https://wttr.in/{city}?format=3", timeout=10)
        if response.status_code == 200:
            return f"Current weather in {response.text.strip()}"
        else:
            return f"Could not retrieve weather for {city} (Status: {response.status_code})"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"

def search_guides_tool(query: str) -> str:
    """
    Searches local travel guides for information.
    
    Args:
        query (str): The search query.
        
    Returns:
        str: Relevant snippets from the guides.
    """
    results = search_guides(query, n_results=3)
    if not results:
        return f"No information found in local guides for: {query}"
    
    combined_results = "\n\n---\n\n".join(results)
    return f"Information found in guides:\n\n{combined_results}"

# --- Tool Definitions for OpenAI API ---

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "budget_breakdown",
            "description": "Calculate a percentage-based breakdown of a travel budget into categories (Accommodation, Food, etc.) and daily average.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The name of the destination city"},
                    "total_budget": {"type": "number", "description": "Total budget for the trip in USD"},
                    "duration_days": {"type": "integer", "description": "Number of days the trip lasts"},
                },
                "required": ["city", "total_budget", "duration_days"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current real-time weather for a specific city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The name of the city (e.g., 'Tokyo', 'Paris')"},
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_guides_tool",
            "description": "Search the local travel guide collection for specific recommendations, tips, or facts about destinations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "The search query or topic to look up in the guides"},
                },
                "required": ["query"],
            },
        },
    }
]

def run_agent(prompt: str) -> str:
    """
    A ReAct agent that uses tools to answer travel questions.
    """
    try:
        from src.ai_assistant import client, MODEL, TRAVEL_SYSTEM_PROMPT
    except ImportError:
        return "AI Agent support not available (could not import client/MODEL)."

    if not client:
        return "AI Agent support not available (OpenAI client not initialized)."

    messages = [
        {"role": "system", "content": TRAVEL_SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    available_tools = {
        "budget_breakdown": budget_breakdown,
        "get_weather": get_weather,
        "search_guides_tool": search_guides_tool,
    }

    # ReAct loop (max 5 iterations)
    for _ in range(5):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOL_DEFINITIONS,
                tool_choice="auto"
            )
        except Exception as e:
            return f"Agent Error: {e}"

        msg = response.choices[0].message
        
        # Handle cases where msg.content might be None but tool_calls exist
        if msg.content:
            messages.append({"role": "assistant", "content": msg.content})
        else:
            # For OpenAI API, tool_calls must be attached to an assistant message
            # If content is None, we still need to record the assistant's intent
            messages.append({"role": "assistant", "content": None, "tool_calls": msg.tool_calls})

        if not msg.tool_calls:
            return msg.content or "The agent finished without an answer."

        # Process tool calls
        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            
            print(f"[Tool call] {name}({args})")
            
            tool_func = available_tools.get(name)
            if tool_func:
                try:
                    result = tool_func(**args)
                except Exception as e:
                    result = f"Error executing tool {name}: {e}"
            else:
                result = f"Error: Tool {name} not found."
            
            print(f"[Tool result] {result[:100]}..." if len(result) > 100 else f"[Tool result] {result}")
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": name,
                "content": result
            })

    return "Agent reached maximum iteration limit."

if __name__ == "__main__":
    # Simple test cases
    print("Testing budget_breakdown:")
    print(budget_breakdown("Tokyo", 5, 1000))
    print("\nTesting get_weather (Tokyo):")
    print(get_weather("Tokyo"))
    print("\nTesting search_guides_tool (Paris):")
    print(search_guides_tool("Paris"))
