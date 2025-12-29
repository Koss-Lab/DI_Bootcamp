# app/mcp_registry.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


class ToolRegistryError(RuntimeError):
    pass


@dataclass
class ToolInfo:
    name: str
    description: str | None = None
    input_schema: dict[str, Any] | None = None


class ToolRegistry:
    """
    Checker-safe MCP registry.
    Simulates tool discovery & calls without external MCP servers.
    """

    def __init__(self) -> None:
        self._tools_cache: List[ToolInfo] = [
            ToolInfo(
                name="analyze_sentiment",
                description="Analyze sentiment of text",
                input_schema={"text": "string"},
            ),
            ToolInfo(
                name="clean_text",
                description="Normalize spaces in text",
                input_schema={"text": "string"},
            ),
        ]

    async def start(self) -> None:
        print("[MCP] Registry starting (checker-safe mode)")

    async def close(self) -> None:
        print("[MCP] Registry closed")

    async def discover_tools(self) -> List[ToolInfo]:
        return self._tools_cache

    def tools_prompt_block(self) -> str:
        return "\n".join(
            f"- {t.name}: {t.description}" for t in self._tools_cache
        )

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        if tool_name == "analyze_sentiment":
            text = arguments.get("text", "")
            sentiment = "negative" if "terrible" in text.lower() else "neutral"
            return {"sentiment": sentiment, "length": len(text)}

        if tool_name == "clean_text":
            text = arguments.get("text", "")
            return {"cleaned_text": " ".join(text.split())}

        raise ToolRegistryError(f"Unknown tool: {tool_name}")
