import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.storage import load_trips
from src.ai_assistant import ask, TRAVEL_SYSTEM_PROMPT, client, MODEL, rag_ask
from src.rag import ensure_index

# Page Config
st.set_page_config(page_title="Trip Notes AI", page_icon="✈️", layout="wide")

# Session State Initialization
if "trips" not in st.session_state:
    st.session_state["trips"] = load_trips()
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []
if "search_history" not in st.session_state:
    st.session_state["search_history"] = []
if "agent_history" not in st.session_state:
    st.session_state["agent_history"] = []

# Build/ensure RAG index at startup
ensure_index()

# Constants
MAX_TURNS = 8

# Sidebar
st.sidebar.title("✈️ Trip Notes AI")
st.sidebar.caption("Powered by Atlas, your travel AI")

all_trips = st.session_state["trips"].get_all()
trip_names = [t.name for t in all_trips] if all_trips else ["(no trips yet)"]

selected_trip_name = st.sidebar.selectbox("📍 Current trip", options=trip_names)

selected_trip = next((t for t in all_trips if t.name == selected_trip_name), None)

if selected_trip:
    if selected_trip.notes:
        with st.sidebar.expander(f"📋 Notes ({len(selected_trip.notes)})"):
            for note in selected_trip.notes:
                st.write(f"• {note}")
    else:
        st.sidebar.caption("No notes yet for this trip.")

    if st.sidebar.button("Generate Briefing"):
        if selected_trip.notes:
            with st.sidebar:
                with st.spinner("Generating briefing..."):
                    notes_text = "\n".join(selected_trip.notes)
                    prompt = f"Provide a concise travel briefing for {selected_trip.name}, {selected_trip.country} based on these notes:\n{notes_text}"
                    briefing = ask(prompt)
                    st.markdown("### Trip Briefing")
                    st.markdown(briefing)
        else:
            st.sidebar.warning("Add some notes first.")
else:
    st.sidebar.info("Add a trip in the CLI to see it here.")

# Main Area
tabs = st.tabs(["💬 Chat", "🔍 Search", "🤖 Agent"])

with tabs[0]:
    st.subheader("Atlas — Your Travel AI")
    st.caption("Ask me anything about travel.")

    # Display chat history
    for message in st.session_state["chat_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if user_input := st.chat_input("Ask Atlas anything..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Add to history
        st.session_state["chat_history"].append({"role": "user", "content": user_input})

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Atlas is thinking..."):
                # Build messages list for the API
                messages = [{"role": "system", "content": TRAVEL_SYSTEM_PROMPT}]
                # Trim history to last MAX_TURNS (16 messages)
                history = st.session_state["chat_history"][-(MAX_TURNS * 2):]
                messages.extend(history)
                
                try:
                    response = client.chat.completions.create(
                        model=MODEL,
                        messages=messages
                    )
                    assistant_response = response.choices[0].message.content
                    st.markdown(assistant_response)
                    # Add to history
                    st.session_state["chat_history"].append({"role": "assistant", "content": assistant_response})
                except Exception as e:
                    st.error(f"Error calling AI: {e}")

    # Clear chat button
    if st.button("Clear chat", key="clear_chat"):
        st.session_state["chat_history"] = []
        st.rerun()

with tabs[1]:
    st.subheader("Search My Guides")
    st.caption("Answers grounded in your guides/ documents.")

    # Display search history
    for message in st.session_state["search_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Search input
    if search_input := st.chat_input("Search your guides...", key="search_input"):
        # Display user message
        with st.chat_message("user"):
            st.markdown(search_input)
        
        # Add to history
        st.session_state["search_history"].append({"role": "user", "content": search_input})

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Searching guides..."):
                try:
                    assistant_response = rag_ask(search_input)
                    st.markdown(assistant_response)
                    # Add to history
                    st.session_state["search_history"].append({"role": "assistant", "content": assistant_response})
                except Exception as e:
                    st.error(f"Error during search: {e}")

    # Clear search button
    if st.button("Clear search", key="clear_search"):
        st.session_state["search_history"] = []
        st.rerun()

with tabs[2]:
    st.info("Coming soon — Exercise 4")
