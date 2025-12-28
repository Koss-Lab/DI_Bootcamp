# 🧠 MCP Smart Data Scout

LLM-powered agent using **MCP (Model Context Protocol)** to dynamically decide and invoke external tools such as **time** and **web fetch**, with a simple **Streamlit UI**.

---

## 🚀 Overview

**MCP Smart Data Scout** demonstrates how a Large Language Model can:

* Analyze a user question
* Decide whether a tool is needed
* Select the appropriate **MCP tool**
* Invoke it through a structured registry
* Return a coherent response to the user

The focus of this project is **agentic orchestration**, not data scraping or RAG.

---

## 🧩 Architecture

```
User (Streamlit UI)
        ↓
   Orchestrator (LLM)
        ↓
   ToolRegistry (MCP)
        ↓
  MCP Tools (time / fetch)
```

### Core components:

* **Orchestrator**: decides whether to answer directly or call a tool
* **ToolRegistry**: registers and exposes MCP tools
* **MCP tools**:

  * `time.now` → current time
  * `fetch.fetch` → fetch web content
* **Streamlit UI**: simple interface to interact with the agent

---

## 🛠️ Technologies

* **Python 3.10+**
* **MCP (Model Context Protocol)**
* **Groq or Ollama** (LLM backend)
* **Streamlit** (UI)

---

## 📂 Project Structure

```
mcp-smart-data-scout/
├── app/
│   ├── orchestrator.py
│   ├── mcp_registry.py
│   ├── main_streamlit.py
│   └── __init__.py
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Create and activate virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment variables (`.env`)

```env
GROQ_API_KEY=your_key_here
# or
OLLAMA_MODEL=llama3
```

---

## ▶️ Run MCP tools (optional – debug mode)

In separate terminals:

```bash
python -m mcp_server_time
python -m mcp_server_fetch
```

---

## 🖥️ Run the Streamlit App

```bash
streamlit run app/main_streamlit.py
```

Open:
👉 [http://localhost:8501](http://localhost:8501)

---

## 🧪 Example Queries

* `what time is it now ?`
* `fetch wikipedia.com`
* `fetch https://example.com`

The agent will **automatically decide** whether to call:

* `time.now`
* `fetch.fetch`

---

## 🧠 Design Choice (Important)

This project intentionally focuses on **tool orchestration**, not on displaying raw tool outputs.

✔ The agent **decides and invokes tools correctly**
✔ Tool calls are **explicit and traceable**
✔ The system is **extensible** and production-oriented

Displaying or post-processing tool outputs can be added easily but is **out of scope for this exercise**.

---

## ✅ Learning Outcomes

* Understand MCP architecture
* Build an agentic LLM system
* Dynamically invoke tools via MCP
* Integrate LLM + tools + UI cleanly

---

## Agentic Flow Example

User input:
"What time is it now?"

Agent steps:
1. LLM plans which tools to use
2. Calls `time.now` MCP server
3. Calls `fetch.fetch` MCP server
4. Calls custom `insights.analyze` MCP server
5. Aggregates results into final response

This demonstrates:
- LLM-driven orchestration
- Multiple third-party MCP servers
- One custom MCP server
- Logging and error handling

---

## 👤 Author

Ariel Kossmann
GenAI & Machine Learning Bootcamp – Mini Project
