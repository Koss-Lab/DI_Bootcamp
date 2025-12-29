# app/mcp_registry.py

from typing import Dict
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters
from app.config import settings


class ToolRegistry:
    """
    Connects to third-party MCP servers and executes tools.
    """

    def __init__(self):
        self.sessions: Dict[str, ClientSession] = {}
        self._contexts = []

    async def start(self):
        await self._connect_stdio(
            "time",
            settings.mcp_time_command,
            settings.mcp_time_args,
        )

        await self._connect_stdio(
            "fetch",
            settings.mcp_fetch_command,
            settings.mcp_fetch_args,
        )

    async def _connect_stdio(self, name: str, command: str, args: list[str]):
        params = StdioServerParameters(command=command, args=args)
        ctx = stdio_client(params)
        self._contexts.append(ctx)

        read, write = await ctx.__aenter__()
        session = ClientSession(read, write)
        await session.initialize()

        self.sessions[name] = session
        print(f"[MCP] Connected to third-party server: {name}")

    async def call_tool(self, tool: str, arguments: dict):
        server_name = tool.split(".")[0]
        session = self.sessions.get(server_name)

        if not session:
            raise RuntimeError(f"No MCP server for tool {tool}")

        print(f"[TOOL] Calling {tool} with {arguments}")
        result = await session.call_tool(tool, arguments)
        print(f"[TOOL] Result: {str(result)[:200]}")

        return result

    async def close(self):
        for ctx in self._contexts:
            await ctx.__aexit__(None, None, None)

        self.sessions.clear()
        self._contexts.clear()
