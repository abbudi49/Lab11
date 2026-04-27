import json
import requests
import sys
import os

# Allow importing from the same directory if run as a script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag import search_guides
from src.ai_assistant import client, MODEL, TRAVEL_SYSTEM_PROMPT

def budget_breakdown(total_budget: float, duration_days: int) -> str:
    """
    Splits a total budget into daily averages and categories.
    
    Args:
        total_budget (float): Total trip budget in USD.
        duration_days (int): Number of days for the trip.
        
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
        f"--- BUDGET BREAKDOWN (${total_budget:,.2f} over {duration_days} days) ---\n"
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
                    "total_budget": {"type": "number", "description": "Total budget for the trip in USD"},
                    "duration_days": {"type": "integer", "description": "Number of days the trip lasts"},
                },
                "required": ["total_budget", "duration_days"],
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

def run_agent(user_prompt: str) -> str:
    """
    A simple ReAct agent that uses the OpenAI tool calling API.
    """
    if not client:
        return "AI Agent Error: No API client configured."

    system_prompt = TRAVEL_SYSTEM_PROMPT + "\nUse the available tools whenever they are relevant to answer the user's question. For example, use 'budget_breakdown' if the user asks for a budget analysis, 'get_weather' for weather inquiries, and 'search_guides_tool' for specific destination info from your guides."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # Map function names to actual Python functions
    available_tools = {
        "budget_breakdown": budget_breakdown,
        "get_weather": get_weather,
        "search_guides_tool": search_guides_tool,
    }

    # Limit to 5 turns to prevent infinite loops
    for i in range(5):
        try:
            # Force tool usage if keywords are found and it's the first turn
            tool_choice = "auto"
            if i == 0:
                if "budget" in user_prompt.lower() or "breakdown" in user_prompt.lower():
                    tool_choice = {"type": "function", "function": {"name": "budget_breakdown"}}
                elif "weather" in user_prompt.lower():
                    tool_choice = {"type": "function", "function": {"name": "get_weather"}}
                elif "guide" in user_prompt.lower() or "search" in user_prompt.lower():
                    tool_choice = {"type": "function", "function": {"name": "search_guides_tool"}}

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                tools=TOOL_DEFINITIONS,
                tool_choice=tool_choice,
            )
        except Exception as e:
            return f"Agent Error: {e}"

        msg = response.choices[0].message
        messages.append(msg)

        if not msg.tool_calls:
            # If no tool calls, this is the final answer
            return msg.content

        # Process each tool call
        for tc in msg.tool_calls:
            name = tc.function.name
            args = json.loads(tc.function.arguments)
            
            print(f"[Tool call] {name}({args})")
            
            func = available_tools.get(name)
            if func:
                result = func(**args)
            else:
                result = f"Error: Tool '{name}' not found."
            
            # Print a snippet of result
            result_snippet = (result[:100] + '...') if len(result) > 100 else result
            print(f"[Tool result] {result_snippet}")
            
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result
            })

    return "Agent Error: Max turns reached without final answer."

if __name__ == "__main__":
    # Simple test cases
    print("Testing budget_breakdown:")
    print(budget_breakdown(1000, 5))
    print("\nTesting get_weather (Tokyo):")
    print(get_weather("Tokyo"))
    print("\nTesting search_guides_tool (Paris):")
    print(search_guides_tool("Paris"))
