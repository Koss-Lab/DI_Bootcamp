import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# LangSmith flags (optional)
# -----------------------------
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2", "false")
os.environ["LANGCHAIN_ENDPOINT"] = os.getenv(
    "LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"
)
os.environ["LANGCHAIN_PROJECT"] = os.getenv(
    "LANGCHAIN_PROJECT", "agentic-rag-streamlit"
)

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="Agentic RAG App", layout="centered")
st.title("🧠 Agentic RAG – Streamlit App")

st.write(
    "Ask a question. The agent will retrieve context and synthesize an answer."
)

question = st.text_input("Your question:")
submitted = st.button("Submit")

# -----------------------------
# Load notebook as text (required)
# -----------------------------
notebook_text = ""
try:
    with open("agentic_rag.ipynb", "r", encoding="utf-8") as f:
        notebook_text = f.read()
except Exception:
    notebook_text = "agentic_rag.ipynb not found yet."

# -----------------------------
# Fake / placeholder agent call
# (expected by the exercise)
# -----------------------------
def call_agent(question: str) -> str:
    """
    This function simulates calling the agent defined in agentic_rag.ipynb.
    In a real setup, this would import a Python API from the notebook or module.
    """
    if not question.strip():
        return "Please enter a question."

    # Simulated response (acceptable per instructions)
    return (
        "This is a simulated agentic RAG response.\n\n"
        f"Question: {question}\n\n"
        "Reasoning: retrieve → read → synthesize.\n"
        "Sources: [simulated]"
    )

# -----------------------------
# Run
# -----------------------------
if submitted:
    with st.spinner("Thinking..."):
        answer = call_agent(question)
        st.success("Answer:")
        st.write(answer)

st.divider()
st.caption("Notebook preview (agentic_rag.ipynb):")
st.text_area("Notebook content", notebook_text[:3000], height=200)
