# app/init.py
"""
Application entrypoint utilities.

This module exists to clearly define how the MCP agent
is initialized and wired together.

It is intentionally lightweight and delegates:
- MCP server management to ToolRegistry
- Planning & execution to Orchestrator
"""

from app.mcp_registry import ToolRegistry
from app.orchestrator import Orchestrator


async def create_agent() -> Orchestrator:
    """
    Factory function that creates a fully initialized agent.

    This function:
    1. Starts MCP servers
    2. Registers available tools
    3. Returns a ready-to-run Orchestrator
    """
    registry = ToolRegistry()
    await registry.start()
    return Orchestrator(registry)
