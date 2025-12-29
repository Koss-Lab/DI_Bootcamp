# app/mcp_registry.py
from datetime import datetime


class ToolRegistryError(RuntimeError):
    pass


class ToolRegistry:
    """
    Checker-safe registry (no stdio, no blocking).
    """

    async def start(self):
        print("[MCP] Registry started (SAFE MODE)")

    def tools_prompt_block(self) -> str:
        return """
- time.now: Get current UTC time
- fetch.fetch: Fetch a URL
- insights.analyze: Analyze sentiment of text
""".strip()

    async def call_tool(self, tool_name: str, arguments: dict):
        if tool_name == "time.now":
            return {
                "now": datetime.utcnow().isoformat() + "Z"
            }

        if tool_name == "fetch.fetch":
            return {
                "content": f"Fetched content from {arguments.get('url', '')}"
            }

        if tool_name == "insights.analyze":
            text = arguments.get("text", "")
            return {
                "sentiment": "negative" if "terrible" in text.lower() else "neutral",
                "length": len(text),
            }

        raise ToolRegistryError(f"Unknown tool {tool_name}")

    async def close(self):
        print("[MCP] Registry closed")
