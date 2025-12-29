# app/mcp_registry.py
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

class MCPRegistry:
    """
    Connects to multiple MCP servers and exposes their tools.
    """

    def __init__(self):
        self.sessions = {}

    async def connect(self, name: str, command: list[str]):
        """
        Start and connect to an MCP server via stdio.
        """
        client = stdio_client(command)
        read, write = await client.__aenter__()
        session = ClientSession(read, write)
        await session.initialize()
        self.sessions[name] = session

    async def call(self, server: str, tool: str, args: dict | None):
        """
        Call a real MCP tool.
        """
        session = self.sessions[server]
        return await session.call_tool(tool, args)
