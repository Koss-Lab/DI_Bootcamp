# app/servers/insights_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("insights")


@mcp.tool()
def analyze(text: str) -> dict:
    """
    Analyze sentiment and length of a text.
    """
    sentiment = "negative" if "terrible" in text.lower() else "neutral"
    return {
        "sentiment": sentiment,
        "length": len(text),
    }


@mcp.tool()
def clean(text: str) -> dict:
    """
    Clean text by normalizing spaces and punctuation.
    """
    cleaned = " ".join(text.strip().split())
    return {"cleaned_text": cleaned}


if __name__ == "__main__":
    mcp.run()
