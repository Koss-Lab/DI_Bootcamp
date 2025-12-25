import os
import sys
import json
from datetime import date
from typing import Any, Dict, List, Optional
import httpx
from dotenv import load_dotenv

load_dotenv()

SERVER_BASE = os.getenv("SERVER_BASE", "http://127.0.0.1:8000").rstrip("/")
TOKEN = os.getenv("MCP_HTTP_TOKEN", "")

DEFAULT_K = 5


def auth_headers() -> Dict[str, str]:
    if not TOKEN:
        raise RuntimeError("MCP_HTTP_TOKEN missing. Set it in .env.")
    return {"Authorization": f"Bearer {TOKEN}"}


def pick_three_distinct_domains(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    picked = []
    seen_domains = set()
    for r in results:
        url = r.get("url") or ""
        try:
            domain = url.split("/")[2].lower()
        except Exception:
            continue
        if domain in seen_domains:
            continue
        seen_domains.add(domain)
        picked.append(r)
        if len(picked) >= 3:
            break
    return picked


def build_markdown(topic: str, summary: Dict[str, Any]) -> str:
    bullets = summary["bullets"]
    sources = summary["sources"]

    lines = []
    lines.append(f"# Briefing: {topic}")
    lines.append("")
    lines.append("## Key points")
    for b in bullets:
        lines.append(f"- {b}")
    lines.append("")
    lines.append("## Sources")
    # Sort by i
    sources_sorted = sorted(sources, key=lambda s: int(s["i"]))
    for s in sources_sorted:
        lines.append(f"[{s['i']}] {s['title']} — {s['url']}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) < 3 or sys.argv[1] != "brief":
        print('Usage: python client.py brief "your topic"')
        return 2

    topic = " ".join(sys.argv[2:]).strip().strip('"')
    if len(topic) < 2:
        print("Topic is too short.")
        return 2

    headers = auth_headers()

    with httpx.Client(timeout=30.0) as client:
        # 1) search_web
        r = client.post(
            f"{SERVER_BASE}/tools/search_web",
            headers=headers,
            json={"query": topic, "k": DEFAULT_K},
        )
        r.raise_for_status()
        results = r.json()["results"]

        # 2) pick 3 domains + fetch_readable
        picked = pick_three_distinct_domains(results)
        if len(picked) < 3:
            picked = results[:3]

        docs = []
        for it in picked:
            fr = client.post(
                f"{SERVER_BASE}/tools/fetch_readable",
                headers=headers,
                json={"url": it["url"]},
            )
            fr.raise_for_status()
            docs.append(fr.json())

        # 3) summarize_with_citations
        sr = client.post(
            f"{SERVER_BASE}/tools/summarize_with_citations",
            headers=headers,
            json={"topic": topic, "docs": docs},
        )
        sr.raise_for_status()
        summary = sr.json()

        # 4) save_markdown
        fname = f"brief_{date.today().isoformat()}.md"
        md = build_markdown(topic, summary)

        sv = client.post(
            f"{SERVER_BASE}/tools/save_markdown",
            headers=headers,
            json={"filename": fname, "content": md},
        )
        sv.raise_for_status()
        path = sv.json()["path"]

    print("Saved:", path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

