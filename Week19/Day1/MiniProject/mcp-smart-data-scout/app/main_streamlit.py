# app/main_streamlit.py
# Streamlit UI for MCP Smart Data Scout
# All code & comments in English (as requested)

import sys
import os

# -------------------------------------------------
# Fix import path so "app.*" works with Streamlit
# -------------------------------------------------
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import streamlit as st

from app.mcp_registry import ToolRegistry
from app.orchestrator import Orchestrator

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="MCP Smart Data Scout",
    page_icon="🧠",
    layout="centered",
)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("🧠 MCP Smart Data Scout")
st.caption("LLM + MCP tools (Groq / Ollama)")
st.write("Ask a question. The agent may decide to call MCP tools.")

# -------------------------------------------------
# Initialize registry & agent (cached)
# -------------------------------------------------
@st.cache_resource
def init_agent():
    registry = ToolRegistry()
    agent = Orchestrator(registry)
    return agent

agent = init_agent()

# -------------------------------------------------
# User input
# -------------------------------------------------
question = st.text_input(
    "Your question",
    placeholder="e.g. What time is it now? or Fetch https://example.com",
)

run_clicked = st.button("Run")

# -------------------------------------------------
# Run agent
# -------------------------------------------------
if run_clicked and question.strip():
    with st.spinner("Thinking..."):
        result = agent.run(question)

    st.subheader("Result")

    # ---------------------------------------------
    # Case 1: Orchestrator returns structured dict
    # ---------------------------------------------
    if isinstance(result, dict):
        tool_used = result.get("tool")
        tool_output = result.get("tool_output")
        final_answer = result.get("final_answer")

        if tool_used:
            st.markdown(f"**🛠 Tool used:** `{tool_used}`")

        if tool_output:
            st.markdown("**📦 Tool output:**")
            st.code(tool_output, language="json" if isinstance(tool_output, dict) else "text")

        if final_answer:
            st.markdown("**✅ Final answer:**")
            st.write(final_answer)

    # ---------------------------------------------
    # Case 2: Plain text fallback
    # ---------------------------------------------
    else:
        st.write(result)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("---")
st.caption("Powered by MCP · Groq / Ollama · Streamlit")
