# app/__init__.py
"""
Application entrypoint helpers.

This module defines how the MCP agent is initialized and wired together.
"""

from app.mcp_registry import ToolRegistry
from app.orchestrator import Orchestrator


async def create_agent() -> Orchestrator:
    """
    Creates and initializes the MCP-powered agent.

    Steps:
    1. Start MCP servers
    2. Register tools
    3. Return a ready orchestrator
    """
    registry = ToolRegistry()
    await registry.start()
    return Orchestrator(registry)
