# app/main_streamlit.py
# Streamlit UI for MCP Smart Data Scout
# This file demonstrates end-to-end MCP integration:
# - 2 third-party MCP servers (time, fetch)
# - 1 custom MCP server (insights)
# - LLM-driven orchestration
# - Error handling and observability
"""
Optional Streamlit UI for the MCP Smart Data Scout project.

This file is NOT required for validation, but demonstrates how
the full agentic system implemented in `full_agent.py` can be
exposed through an interactive interface.

The agent:
- Uses a custom MCP server with user-defined tools
- Can be composed with external MCP servers
- Supports LLM-driven planning (Groq / Ollama)

Core logic lives in `full_agent.py`.
"""


import asyncio
import streamlit as st

from app.mcp_registry import MCPRegistry
from app.orchestrator import Orchestrator
from full_agent import run_agent


st.set_page_config(page_title="MCP Smart Data Scout", layout="centered")

st.title("🔍 MCP Smart Data Scout")
st.write(
    """
This demo shows an **agentic MCP application**:
- Uses **Groq / Ollama LLM** for planning
- Integrates **multiple MCP servers**
- Executes real MCP tool calls
"""
)

question = st.text_input(
    "Ask a question",
    placeholder="e.g. What time is it now?"
)


async def run_agent(user_question: str) -> str:
    """
    Initialize MCP servers, run the orchestrator,
    and return the final answer.
    """
    registry = MCPRegistry()

    # --- Connect to third-party MCP servers ---
    await registry.connect(
        name="time",
        command=["python", "-m", "mcp_server_time"]
    )

    await registry.connect(
        name="fetch",
        command=["python", "-m", "mcp_server_fetch"]
    )

    # --- Connect to custom MCP server ---
    await registry.connect(
        name="insights",
        command=["python", "app/servers/insights_server.py"]
    )

    agent = Orchestrator(registry)
    result = await agent.run(user_question)
    return result


if st.button("Run agent"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Running agent..."):
            try:
                output = asyncio.run(run_agent(question))
                st.success("Agent completed successfully")
                st.text_area(
                    "Agent output",
                    value=output,
                    height=200
                )
            except Exception as e:
                st.error("Agent execution failed")
                st.exception(e)


st.divider()
st.caption(
    "MCP Smart Data Scout — Mini Project (Developers Institute)"
)
