# HTTP Web Search Briefing Bot

This project implements a tiny **HTTP-only briefing bot** exposing MCP-style "tool" endpoints.
A CLI client orchestrates the full flow end-to-end and saves a Markdown briefing with citations.

---

## What this project does

The server exposes the following HTTP JSON tools (authenticated via Bearer token):

- `GET /tools`
- `POST /tools/search_web`
- `POST /tools/fetch_readable`
- `POST /tools/summarize_with_citations`
- `POST /tools/save_markdown`

The CLI client calls them in order to produce a reproducible research briefing.

---

## Architecture

CLI (client.py) │ ├── HTTP → /tools/search_web ──→ Tavily Search API (free) ├── HTTP → /tools/fetch_readable ──→ trafilatura (main content extraction) ├── HTTP → /tools/summarize_with_citations ──→ Local LLM (Ollama) └── HTTP → /tools/save_markdown ──→ Disk (outputs/)
All communication is **HTTP only** (no stdio).

---

## Prerequisites

- Python 3.10+
- A free Tavily API key
- A local LLM running over HTTP:
  - **Ollama** (default), or
  - LM Studio (OpenAI-compatible)

---

## Installation (under 10 minutes)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Create your environment file:
cp .env.example .env
Fill in:
MCP_HTTP_TOKEN
TAVILY_API_KEY

Local LLM setup (Ollama)
Install Ollama: https://ollama.com
Pull and run a model:
ollama pull llama3
ollama run llama3
Ollama exposes an HTTP API at:
http://127.0.0.1:11434

Run the server
source .venv/bin/activate
uvicorn server:app --host 127.0.0.1 --port 8000
Health check:
curl http://127.0.0.1:8000/healthz

Run the CLI client
source .venv/bin/activate
python client.py brief "Latest AI regulation in Europe"
Output:
Saved: outputs/brief_YYYY-MM-DD.md

Sample Output
A sample Markdown briefing is generated in:
outputs/brief_YYYY-MM-DD.md
It contains:
Exactly 5 bullets
Inline citation markers [1], [2], etc.
A sources section mapping citations to URLs

API Endpoints (cURL examples)
List tools
curl http://127.0.0.1:8000/tools \
  -H "Authorization: Bearer <MCP_HTTP_TOKEN>"
Search web
curl http://127.0.0.1:8000/tools/search_web \
  -H "Authorization: Bearer <MCP_HTTP_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"query":"AI regulation Europe","k":5}'
Fetch readable page
curl http://127.0.0.1:8000/tools/fetch_readable \
  -H "Authorization: Bearer <MCP_HTTP_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
Summarize with citations
curl http://127.0.0.1:8000/tools/summarize_with_citations \
  -H "Authorization: Bearer <MCP_HTTP_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"topic":"Example topic","docs":[{"url":"https://example.com","title":"Example","text":"Long text..."}]}'
Save Markdown
curl http://127.0.0.1:8000/tools/save_markdown \
  -H "Authorization: Bearer <MCP_HTTP_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"filename":"brief_test.md","content":"# Example"}'

Security Notes
Secrets are stored in .env (not committed)
Authentication enforced via Bearer token
Filename sanitization prevents path traversal
HTTP timeouts and retries are enabled

Deliverables Checklist
HTTP server with required endpoints
CLI client automating the full flow
Local LLM via HTTP (Ollama)
Markdown output with citations
README with setup and examples
Sample output file

© 2025 Developers Institute – Daily Challenge
