"""
MCP Tool Registry

- Connects to third-party MCP servers (stdio)
- Discovers tools
- Executes tool calls
- Provides a clean abstraction for the Orchestrator
"""

import asyncio
from typing import Dict

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

from app.config import settings


# ============================================================
# Exceptions
# ============================================================

class ToolRegistryError(Exception):
    """Raised when a tool registry operation fails."""
    pass


# ============================================================
# Tool Registry
# ============================================================

class ToolRegistry:
    """
    Manages MCP server connections and tool execution.
    """

    def __init__(self) -> None:
        self.sessions: Dict[str, ClientSession] = {}
        self._transports = []

    # --------------------------------------------------------
    # Startup / Shutdown
    # --------------------------------------------------------

    async def start(self) -> None:
        """
        Start all configured MCP servers.
        """
        await self._connect_stdio(
            name="time",
            command=settings.mcp_time_command,
            args=settings.mcp_time_args_list,
        )

        await self._connect_stdio(
            name="fetch",
            command=settings.mcp_fetch_command,
            args=settings.mcp_fetch_args_list,
        )

    async def close(self) -> None:
        """
        Gracefully close all MCP sessions.
        """
        for session in self.sessions.values():
            await session.close()

        for transport in self._transports:
            await transport.__aexit__(None, None, None)

    # --------------------------------------------------------
    # Internal connection helpers
    # --------------------------------------------------------

    async def _connect_stdio(self, name: str, command: str, args: list[str]) -> None:
        """
        Connect to a stdio-based MCP server.
        """
        try:
            params = StdioServerParameters(
                command=command,
                args=args,
            )

            transport_cm = stdio_client(params)
            read, write = await transport_cm.__aenter__()

            session = ClientSession(read, write)
            await session.initialize()

            self.sessions[name] = session
            self._transports.append(transport_cm)

        except Exception as e:
            raise ToolRegistryError(
                f"Failed to start MCP server '{name}': {e}"
            ) from e

    # --------------------------------------------------------
    # Tool discovery & execution
    # --------------------------------------------------------

    async def list_tools(self) -> dict[str, list[str]]:
        """
        List tools exposed by each connected MCP server.
        """
        tools: dict[str, list[str]] = {}

        for name, session in self.sessions.items():
            try:
                result = await session.list_tools()
                tools[name] = [tool.name for tool in result.tools]
            except Exception as e:
                tools[name] = []
                print(f"[WARN] Failed to list tools for {name}: {e}")

        return tools

    async def call_tool(
        self,
        server: str,
        tool: str,
        arguments: dict | None = None,
    ):
        """
        Execute a tool on a given MCP server.
        """
        if server not in self.sessions:
            raise ToolRegistryError(f"Server '{server}' is not connected")

        try:
            session = self.sessions[server]
            return await session.call_tool(tool, arguments or {})
        except Exception as e:
            raise ToolRegistryError(
                f"Tool call failed: {server}.{tool} → {e}"
            ) from e
