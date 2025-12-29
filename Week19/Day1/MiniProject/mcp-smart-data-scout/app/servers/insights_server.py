# app/servers/insights_server.py
from __future__ import annotations

import re
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server


server = Server("insights")


@server.tool()
def analyze_sentiment(text: str) -> dict[str, Any]:
    """
    Basic sentiment heuristic.
    Input:
      - text: string
    Output:
      - sentiment: "positive"|"negative"|"neutral"
      - length: int
    """
    t = text.lower()
    neg = any(w in t for w in ["terrible", "rude", "bad", "awful", "hate", "worst"])
    pos = any(w in t for w in ["great", "good", "amazing", "love", "excellent", "best"])

    if neg and not pos:
        s = "negative"
    elif pos and not neg:
        s = "positive"
    else:
        s = "neutral"

    return {"sentiment": s, "length": len(text)}


@server.tool()
def clean_text(text: str) -> dict[str, Any]:
    """
    Simple cleanup:
    - trims
    - collapses whitespace
    - removes repeated punctuation
    """
    original_len = len(text)
    t = text.strip()
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"([!?.,])\1{1,}", r"\1", t)
    return {"cleaned": t, "original_len": original_len, "cleaned_len": len(t)}


def main() -> None:
    # stdio transport
    stdio_server(server)


if __name__ == "__main__":
    main()
