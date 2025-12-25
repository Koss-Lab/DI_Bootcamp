# HTTP Web Search Briefing Bot (MCP-style tools)

Tiny HTTP server exposing 4 JSON "tool" endpoints:
- GET /tools
- POST /tools/search_web
- POST /tools/fetch_readable
- POST /tools/summarize_with_citations
- POST /tools/save_markdown

Auth: `Authorization: Bearer <MCP_HTTP_TOKEN>`

## Prereqs
- Python 3.10+
- A free web search API key (Tavily recommended)
- A local LLM over HTTP:
  - Ollama (default), or
  - LM Studio (OpenAI-compatible)

## Setup (under 10 minutes)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # or create .env manually

