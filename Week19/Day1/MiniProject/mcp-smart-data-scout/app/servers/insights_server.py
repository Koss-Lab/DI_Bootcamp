# app/servers/insights_server.py
"""
Custom MCP Server: Insights Server

This MCP server exposes custom tools designed to enrich and analyze text.
It is intended to be composed with third-party MCP servers (e.g. time, fetch)
inside an LLM-driven agentic workflow.
"""

from typing import Dict
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="insights",
    description=(
        "Custom MCP server providing text cleaning, enrichment, "
        "and sentiment analysis tools for agentic workflows."
    ),
)


@mcp.tool(
    description=(
        "Normalize and clean raw text input. "
        "This tool prepares text for downstream analysis by agents."
    )
)
def clean_text(text: str) -> Dict[str, str]:
    """
    Clean and normalize a raw text string.

    Steps:
    - Trim leading/trailing whitespace
    - Normalize repeated spaces
    - Remove basic punctuation noise

    Args:
        text (str): Raw input text

    Returns:
        dict:
            cleaned_text (str): Normalized version of the input
    """
    cleaned = " ".join(text.strip().replace("!", "").replace("?", "").split())
    return {
        "cleaned_text": cleaned
    }


@mcp.tool(
    description=(
        "Analyze sentiment and basic statistics of a text. "
        "This tool adds semantic insight useful for decision-making agents."
    )
)
def analyze_text(text: str) -> Dict[str, object]:
    """
    Perform basic sentiment analysis and metadata extraction.

    Args:
        text (str): Cleaned or raw text

    Returns:
        dict:
            sentiment (str): 'positive', 'negative', or 'neutral'
            length (int): Character length of the text
            contains_warning (bool): Heuristic flag for problematic language
    """
    lowered = text.lower()

    sentiment = "neutral"
    if any(w in lowered for w in ["terrible", "bad", "awful", "hate"]):
        sentiment = "negative"
    elif any(w in lowered for w in ["great", "excellent", "love", "amazing"]):
        sentiment = "positive"

    return {
        "sentiment": sentiment,
        "length": len(text),
        "contains_warning": sentiment == "negative",
    }


if __name__ == "__main__":
    # Run the MCP server locally over stdio
    mcp.run()
