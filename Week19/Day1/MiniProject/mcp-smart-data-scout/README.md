# MCP Smart Data Scout

This project is an end-to-end agentic application built using the Model Context Protocol (MCP).

## Overview

The application integrates multiple third-party MCP servers from the community ecosystem and orchestrates them using an LLM-driven agent.

## Integrated MCP Servers (Third-Party)

- **mcp_server_time** – community MCP server for time-related queries
- **mcp_server_fetch** – community MCP server for HTTP fetching

These servers are run locally and connected via an MCP client using stdio transport.

## Custom MCP Tool

- **insights.analyze** – local analysis tool for text insights

## Architecture

1. User provides a goal
2. LLM plans which tool to call
3. MCP client executes the tool
4. Results are logged and returned
5. Errors are handled with retries

## LLM Backend

The orchestrator supports:
- GroqCloud (hosted LLMs)
- Ollama (local models)

Configuration is environment-based.

## Observability

Each tool call is logged with:
- tool name
- summarized input
- summarized output

No secrets are logged.

## Reproducibility

```bash
python -m venv .venv
source .venv/bin/activate
pip install mcp
python app/main_streamlit.py
````

## Example

```python
TIME => time.now → 2025-12-29T11:50:38Z
ANALYZE => insights.analyze → negative sentiment
```

```
