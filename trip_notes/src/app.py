import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from src.storage import load_trips
from src.ai_assistant import ask, TRAVEL_SYSTEM_PROMPT, client

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
    st.info("Coming soon — Exercise 2")

with tabs[1]:
    st.info("Coming soon — Exercise 3")

with tabs[2]:
    st.info("Coming soon — Exercise 4")
