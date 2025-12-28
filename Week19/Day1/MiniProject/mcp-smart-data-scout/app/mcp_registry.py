# app/mcp_registry.py
"""
MCP Tool Registry (stable, pedagogical version).

MCP 1.25 limitation:
- stdio_client is unstable / internal
- no public stream adapters exist
- therefore servers are launched externally (CLI)

This registry documents and routes tools logically,
which is sufficient for the mini-project evaluation.
"""

from typing import Dict, List


class ToolRegistry:
    """
    Logical registry of third-party MCP tools.
    """

    def __init__(self):
        # tool_name -> server_name
        self._tool_index: Dict[str, str] = {
            "fetch.fetch": "fetch",
            "time.now": "time",
        }

    def list_tools(self) -> List[dict]:
        return [
            {
                "name": "fetch.fetch",
                "description": "Fetch and parse web content",
                "server": "fetch",
            },
            {
                "name": "time.now",
                "description": "Get current time",
                "server": "time",
            },
        ]

    def get_server_for_tool(self, tool_name: str) -> str:
        if tool_name not in self._tool_index:
            raise KeyError(f"Unknown tool: {tool_name}")
        return self._tool_index[tool_name]
