from typing import Dict


def analyze(text: str) -> Dict[str, str]:
    """
    Custom MCP-style analysis tool.

    Performs a simple sentiment classification to demonstrate
    how a custom server integrates into the agent flow.
    """

    sentiment = "negative" if "terrible" in text.lower() else "neutral"

    return {
        "sentiment": sentiment,
        "summary": text[:120],
    }
