# MCP Smart Data Scout

Mini-project for **Week 19 – Day 1**  
GenAI & Machine Learning Bootcamp – Developers Institute

---

## 🎯 Project Overview

**MCP Smart Data Scout** is an **agentic application** built on top of the **Model Context Protocol (MCP)**.  
The agent uses a **Large Language Model (LLM)** to dynamically plan and orchestrate calls to multiple MCP servers in order to answer user queries.

The project demonstrates:
- Integration of **multiple third-party MCP servers**
- A **custom MCP server**
- **LLM-driven planning**
- **Tool orchestration**
- **Error handling & configuration**
- A **Streamlit UI** for interaction

---

## 🧠 Architecture

```

User (CLI / Streamlit)
│
▼
Orchestrator (LLM-driven)
│
▼
ToolRegistry
│
├── MCP Time Server (3rd-party)
├── MCP Fetch Server (3rd-party)
└── Insights Server (custom)



---

## 🔧 MCP Servers Used

### 1️⃣ Third-party MCP Servers

- **Time MCP Server**
  - Provides current time information
  - Started via `mcp_server_time`

- **Fetch MCP Server**
  - Fetches remote HTTP resources
  - Started via `mcp_server_fetch`

### 2️⃣ Custom MCP Server

- **Insights Server**
  - Custom server implemented in this repository
  - Performs simple text analysis / sentiment inspection
  - Demonstrates how to expose a custom capability via MCP

---

## 🤖 LLM-Driven Orchestration

The agent:
1. Receives a natural language query
2. Uses an LLM (Groq or Ollama) to **plan which tools are needed**
3. Executes tool calls via MCP
4. Handles errors gracefully
5. Returns the final result

Tool execution order is **not hard-coded**; it is decided dynamically based on the user query.

---

## ⚙️ Configuration

All configuration is handled via environment variables and `app/config.py`.

### Supported LLM Backends
- **GroqCloud** (default)
- **Ollama** (local)

### Example `.env`
```env
LLM_BACKEND=groq
GROQ_API_KEY=your_api_key_here
````

> ⚠️ `.env` is intentionally ignored by Git.

---
## Installation

This project uses Python 3.10+ and relies on the following packages:

- mcp
- pydantic
- pydantic-settings
- httpx
- streamlit

### Setup example

```bash
python -m venv .venv
source .venv/bin/activate
pip install mcp pydantic pydantic-settings httpx streamlit
````

### Running the app

```bash
streamlit run app/main_streamlit.py
```


### 3️⃣ (Optional) Verify MCP Time Server

```bash
python3 -m mcp_server_time --local-timezone UTC
```

---

## ▶️ Running the Agent (CLI)

```bash
python3 - << 'EOF'
from app.orchestrator import Orchestrator
from app.mcp_registry import ToolRegistry
import asyncio

async def main():
    registry = ToolRegistry()
    await registry.start()

    agent = Orchestrator(registry)

    print(await agent.run_async("What time is it now?"))
    print(await agent.run_async("Analyze: The service was terrible and the staff was rude."))

    await registry.close()

asyncio.run(main())
EOF
```

> Note:
> Tool execution is **MCP-driven**.
> Successful execution may not always produce a printed string, but tool calls are executed correctly.

---

## 🌐 Running the Streamlit App

```bash
streamlit run app/main_streamlit.py
```

Then open:

```
http://localhost:8501
```

The Streamlit UI allows interactive querying of the agent.

---

## 🛡️ Error Handling & Observability

* MCP server startup failures are handled gracefully
* Tool execution is wrapped in try/except blocks
* Configuration errors are validated via Pydantic
* Tool calls can be logged and summarized without exposing secrets

---

## 📁 Project Structure

```
mcp-smart-data-scout/
├── app/
│   ├── config.py
│   ├── llm_client.py
│   ├── mcp_registry.py
│   ├── orchestrator.py
│   ├── main_streamlit.py
│   └── servers/
│       └── insights_server.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ✅ Project Requirements Checklist

* [x] At least **two third-party MCP servers**
* [x] One **custom MCP server**
* [x] **LLM-driven planning**
* [x] MCP orchestration
* [x] Error handling
* [x] Environment-based configuration
* [x] Streamlit interface
* [x] Reproducible setup

---

## 🏁 Final Notes

This project focuses on **architecture and orchestration**, not UI polish.
Successful execution is demonstrated through:

* MCP server startup
* Tool calls
* LLM-based planning

---

**Author:** Ariel Kossmann
**Bootcamp:** Developers Institute – GenAI & ML

