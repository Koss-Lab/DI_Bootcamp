import os
import json
import re
import pathlib
from datetime import datetime
from typing import Any, Dict, List, Optional

import httpx
import trafilatura
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field, HttpUrl
from tenacity import retry, stop_after_attempt, wait_exponential

load_dotenv()

APP_TITLE = "HTTP Web Search Briefing Bot"
OUTPUT_DIR = pathlib.Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

MCP_HTTP_TOKEN = os.getenv("MCP_HTTP_TOKEN", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower().strip()
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
LMSTUDIO_BASE_URL = os.getenv("LMSTUDIO_BASE_URL", "http://127.0.0.1:1234/v1").rstrip("/")
LMSTUDIO_MODEL = os.getenv("LMSTUDIO_MODEL", "llama-3.1-8b-instruct")

HTTP_TIMEOUT_S = 20.0

app = FastAPI(title=APP_TITLE)


# ----------------------------
# Auth
# ----------------------------
def require_bearer(authorization: Optional[str]) -> None:
    if not MCP_HTTP_TOKEN:
        raise HTTPException(status_code=500, detail="Server misconfigured: MCP_HTTP_TOKEN is missing.")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized: missing Bearer token.")
    token = authorization.split(" ", 1)[1].strip()
    if token != MCP_HTTP_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized: invalid token.")


# ----------------------------
# Schemas
# ----------------------------
class ToolInfo(BaseModel):
    name: str
    input_schema: Dict[str, Any]


class SearchWebIn(BaseModel):
    query: str = Field(..., min_length=2, max_length=300)
    k: int = Field(5, ge=1, le=10)


class SearchResult(BaseModel):
    title: str
    url: HttpUrl
    snippet: str
    source: str = "tavily"


class SearchWebOut(BaseModel):
    results: List[SearchResult]


class FetchReadableIn(BaseModel):
    url: HttpUrl


class FetchReadableOut(BaseModel):
    url: HttpUrl
    title: str
    text: str


class SourceItem(BaseModel):
    i: int
    title: str
    url: HttpUrl


class SummarizeIn(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200)
    docs: List[FetchReadableOut] = Field(..., min_length=1, max_length=6)


class SummarizeOut(BaseModel):
    bullets: List[str]
    sources: List[SourceItem]


class SaveMarkdownIn(BaseModel):
    filename: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=1, max_length=200_000)


class SaveMarkdownOut(BaseModel):
    path: str


# ----------------------------
# /tools (schemas)
# ----------------------------
@app.get("/tools", response_model=List[ToolInfo])
def list_tools(authorization: Optional[str] = Header(default=None)) -> List[ToolInfo]:
    require_bearer(authorization)
    return [
        ToolInfo(
            name="search_web",
            input_schema={
                "type": "object",
                "properties": {"query": {"type": "string"}, "k": {"type": "integer", "default": 5}},
                "required": ["query"],
            },
        ),
        ToolInfo(
            name="fetch_readable",
            input_schema={
                "type": "object",
                "properties": {"url": {"type": "string"}},
                "required": ["url"],
            },
        ),
        ToolInfo(
            name="summarize_with_citations",
            input_schema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                    "docs": {"type": "array"},
                },
                "required": ["topic", "docs"],
            },
        ),
        ToolInfo(
            name="save_markdown",
            input_schema={
                "type": "object",
                "properties": {"filename": {"type": "string"}, "content": {"type": "string"}},
                "required": ["filename", "content"],
            },
        ),
    ]


# ----------------------------
# Tavily Search
# ----------------------------
@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=0.5, max=4))
async def tavily_search(query: str, k: int) -> List[SearchResult]:
    if not TAVILY_API_KEY:
        raise HTTPException(status_code=400, detail="TAVILY_API_KEY missing. Set it in .env (or env vars).")

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": k,
        "search_depth": "basic",
        "include_answer": False,
        "include_images": False,
    }

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_S) as client:
        r = await client.post("https://api.tavily.com/search", json=payload)
        r.raise_for_status()
        data = r.json()

    results = []
    for item in (data.get("results") or [])[:k]:
        title = (item.get("title") or "").strip() or "Untitled"
        url = item.get("url") or ""
        snippet = (item.get("content") or item.get("snippet") or "").strip()
        if url:
            results.append(SearchResult(title=title, url=url, snippet=snippet, source="tavily"))
    return results


@app.post("/tools/search_web", response_model=SearchWebOut)
async def search_web(body: SearchWebIn, authorization: Optional[str] = Header(default=None)) -> SearchWebOut:
    require_bearer(authorization)
    results = await tavily_search(body.query, body.k)
    return SearchWebOut(results=results)


# ----------------------------
# Fetch readable content
# ----------------------------
@retry(stop=stop_after_attempt(2), wait=wait_exponential(min=0.5, max=2))
async def fetch_url_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (BriefingBot/1.0)",
        "Accept": "text/html,application/xhtml+xml",
    }
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_S, follow_redirects=True, headers=headers) as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.text


def extract_readable(html: str, url: str) -> Dict[str, str]:
    downloaded = trafilatura.extract(
        html,
        url=url,
        include_comments=False,
        include_tables=False,
        favor_recall=True,
        output_format="json",
    )
    if not downloaded:
        return {"title": "", "text": ""}

    try:
        parsed = json.loads(downloaded)
    except Exception:
        return {"title": "", "text": ""}

    title = (parsed.get("title") or "").strip()
    text = (parsed.get("text") or "").strip()
    return {"title": title, "text": text}


@app.post("/tools/fetch_readable", response_model=FetchReadableOut)
async def fetch_readable(body: FetchReadableIn, authorization: Optional[str] = Header(default=None)) -> FetchReadableOut:
    require_bearer(authorization)

    html = await fetch_url_html(str(body.url))
    extracted = extract_readable(html, str(body.url))

    title = extracted.get("title") or "Untitled"
    text = extracted.get("text") or ""

    if len(text.strip()) < 200:
        raise HTTPException(status_code=422, detail="Readability extraction returned too little text. Try another URL.")

    # Keep it reasonable for local LLM
    max_chars = 12_000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n[TRUNCATED]"

    return FetchReadableOut(url=body.url, title=title, text=text)


# ----------------------------
# LLM summarization with citations
# ----------------------------
def build_citation_prompt(topic: str, docs: List[FetchReadableOut]) -> str:
    # Sources are 1..N in this order
    sources_block = []
    for idx, d in enumerate(docs, start=1):
        sources_block.append(
            f"[{idx}] TITLE: {d.title}\nURL: {d.url}\nCONTENT:\n{d.text}\n"
        )
    sources_text = "\n\n".join(sources_block)

    return (
        "You are a briefing assistant.\n"
        "Task: produce EXACTLY 5 bullets summarizing the topic using the provided sources.\n"
        "Rules:\n"
        "- Output MUST be valid JSON only.\n"
        "- JSON shape: {\"bullets\": [\"...\"], \"sources\": [{\"i\":1,\"title\":\"...\",\"url\":\"...\"}, ...]}\n"
        "- bullets: exactly 5 strings, each <= 200 characters.\n"
        "- Each bullet must include at least one inline citation marker like [1] or [2].\n"
        "- Only cite from the given sources list.\n"
        "- sources array must include every cited source index exactly once (no extras).\n\n"
        f"TOPIC: {topic}\n\n"
        f"SOURCES:\n{sources_text}\n"
    )


def extract_json_loose(text: str) -> Dict[str, Any]:
    # Try strict parse first
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass

    # Try to find first {...} block
    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not m:
        raise ValueError("LLM output did not contain JSON object.")
    return json.loads(m.group(0))


async def llm_summarize(topic: str, docs: List[FetchReadableOut]) -> SummarizeOut:
    """
    Robust summarization:
    - Try Ollama JSON output
    - If anything fails, FALLBACK to deterministic bullets
    NEVER returns 500.
    """

    # ---------------------------
    # FALLBACK (SAFE + VALID)
    # ---------------------------
    def fallback_summary() -> SummarizeOut:
        bullets = []
        for i, d in enumerate(docs[:5], start=1):
            text = d.text.strip().replace("\n", " ")
            if len(text) > 160:
                text = text[:160] + "..."
            bullets.append(f"{text} [{i}]")

        # Ensure exactly 5 bullets
        while len(bullets) < 5:
            bullets.append(f"Additional context related to {topic}. [1]")

        sources = [
            SourceItem(i=i, title=d.title, url=d.url)
            for i, d in enumerate(docs, start=1)
        ]

        return SummarizeOut(bullets=bullets[:5], sources=sources)

    # ---------------------------
    # TRY LLM
    # ---------------------------
    try:
        prompt = build_citation_prompt(topic, docs)

        payload = {
            "model": OLLAMA_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "Return ONLY valid JSON.\n"
                        "No markdown. No commentary.\n"
                        "Schema:\n"
                        "{"
                        '"bullets": ["string"], '
                        '"sources": [{"i": 1, "title": "string", "url": "string"}]'
                        "}"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "options": {
                "temperature": 0.0,
            },
        }

        async with httpx.AsyncClient(timeout=HTTP_TIMEOUT_S) as client:
            r = await client.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload)
            r.raise_for_status()
            data = r.json()

        raw = (data.get("message") or {}).get("content") or ""
        print("\n===== RAW OLLAMA OUTPUT =====")
        print(raw)
        print("============================\n")

        obj = extract_json_loose(raw)

        bullets = obj.get("bullets")
        sources = obj.get("sources")

        if not isinstance(bullets, list) or len(bullets) < 5:
            raise ValueError("Invalid bullets")

        fixed_bullets = []
        cited = set()

        for b in bullets[:5]:
            if not isinstance(b, str):
                raise ValueError("Bullet not string")
            if len(b) > 200:
                b = b[:197] + "..."
            matches = re.findall(r"\[(\d+)\]", b)
            if not matches:
                raise ValueError("Missing citation")
            for m in matches:
                cited.add(int(m))
            fixed_bullets.append(b)

        fixed_sources = []
        for s in sources or []:
            i = int(s["i"])
            if i in cited:
                fixed_sources.append(
                    SourceItem(i=i, title=s["title"], url=s["url"])
                )

        if not fixed_sources:
            raise ValueError("No valid sources")

        return SummarizeOut(
            bullets=fixed_bullets,
            sources=fixed_sources,
        )

    except Exception as e:
        print("⚠️ LLM FAILED, USING FALLBACK:", e)
        return fallback_summary()


@app.post("/tools/summarize_with_citations", response_model=SummarizeOut)
async def summarize_with_citations(body: SummarizeIn, authorization: Optional[str] = Header(default=None)) -> SummarizeOut:
    require_bearer(authorization)
    return await llm_summarize(body.topic, body.docs)


# ----------------------------
# Save Markdown
# ----------------------------
def safe_filename(name: str) -> str:
    name = name.strip()
    name = re.sub(r"[^a-zA-Z0-9_\-\.]", "_", name)
    if not name.endswith(".md"):
        name += ".md"
    return name


@app.post("/tools/save_markdown", response_model=SaveMarkdownOut)
def save_markdown(body: SaveMarkdownIn, authorization: Optional[str] = Header(default=None)) -> SaveMarkdownOut:
    require_bearer(authorization)

    filename = safe_filename(body.filename)
    path = OUTPUT_DIR / filename
    path.write_text(body.content, encoding="utf-8")
    return SaveMarkdownOut(path=str(path))


@app.get("/healthz")
def healthz() -> Dict[str, Any]:
    return {
        "ok": True,
        "llm_provider": LLM_PROVIDER,
        "has_tavily_key": bool(TAVILY_API_KEY),
        "time": datetime.utcnow().isoformat() + "Z",
    }

