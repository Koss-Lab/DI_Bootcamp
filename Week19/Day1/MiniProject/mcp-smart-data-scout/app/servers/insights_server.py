# app/servers/insights_server.py
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("insights")

@server.tool()
def analyze(text: str) -> TextContent:
    """
    Analyze text and return simple insights.
    """
    if not text:
        return TextContent(text="No text provided")

    return TextContent(text=f"Text length: {len(text)} characters")

if __name__ == "__main__":
    server.run()
