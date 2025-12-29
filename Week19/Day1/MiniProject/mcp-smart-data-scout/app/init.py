# app/init.py
"""
Application entry-point placeholder.

This module demonstrates how the MCP registry and agent
can be initialized together.

Full agentic logic is implemented in full_agent.py.
"""

from app.mcp_registry import ToolRegistry

def init_app() -> ToolRegistry:
    """
    Initialize the MCP registry.
    """
    return ToolRegistry()
