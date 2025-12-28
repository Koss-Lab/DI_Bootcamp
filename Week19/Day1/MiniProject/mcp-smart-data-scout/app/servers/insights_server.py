# app/servers/insights_server.py

def analyze(text: str) -> str:
    """
    Simple custom MCP server.
    Provides basic insight from user text.
    """
    if not text:
        return "No text provided."

    return f"Text length: {len(text)} characters"
