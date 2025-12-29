from __future__ import annotations

"""
Custom MCP server exposing an 'insights.analyze' tool.
This represents the user's own MCP server (local).
"""

from typing import Any, Dict

# MCP server API (best-effort imports depending on version)
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
except Exception as e:
    raise RuntimeError(f"Cannot import MCP server modules. Is 'mcp' installed? {e}")


server = Server("insights")


def _basic_insights(text: str) -> Dict[str, Any]:
    # Tiny deterministic analysis (no external deps)
    t = (text or "").strip()
    lower = t.lower()

    positives = ["good", "great", "love", "excellent", "amazing", "happy"]
    negatives = ["bad", "terrible", "hate", "awful", "sad", "rude"]

    score = 0
    for p in positives:
        if p in lower:
            score += 1
    for n in negatives:
        if n in lower:
            score -= 1

    sentiment = "neutral"
    if score > 0:
        sentiment = "positive"
    elif score < 0:
        sentiment = "negative"

    return {
        "sentiment": sentiment,
        "score": score,
        "length": len(t),
        "preview": t[:160],
    }


@server.tool("insights.analyze")
async def analyze_tool(text: str) -> Dict[str, Any]:
    return _basic_insights(text)


async def main() -> None:
    async with stdio_server(server):
        await server.run()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
