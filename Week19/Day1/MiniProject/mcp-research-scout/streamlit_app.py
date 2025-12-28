# streamlit_app.py

import streamlit as st
from app.orchestrator import run_agent

st.set_page_config(page_title="MCP Research Scout", layout="wide")

st.title("MCP Research Scout")
st.caption("Agentic AI using multiple MCP servers")

goal = st.text_area(
    "User goal",
    value=(
        "Fetch a web page about Model Context Protocol, "
        "summarize key ideas, and save a brief in the workspace."
    ),
    height=120,
)

if st.button("Run agent"):
    with st.spinner("Agent is thinking..."):
        answer, logs = run_agent(goal)

    st.subheader("Final Answer")
    st.write(answer)

    st.subheader("Execution Logs")
    st.json(logs)
