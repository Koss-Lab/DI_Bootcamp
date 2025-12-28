# app/mcp_multi.py

import sys
from typing import Dict, Tuple

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters


class MultiMCP:
    def __init__(self):
        self._clients = {}
        self._sessions: Dict[str, ClientSession] = {}

    async def __aenter__(self):
        print(">>> [MCP] Connecting to servers...")

        servers = {
            "fetch": StdioServerParameters(
                command=sys.executable,
                args=["-m", "mcp_server_fetch"],
            ),
            "time": StdioServerParameters(
                command=sys.executable,
                args=["-m", "mcp_server_time", "--local-timezone", "Asia/Jerusalem"],
            ),
        }

        for name, params in servers.items():
            client_cm = stdio_client(params)
            read, write = await client_cm.__aenter__()

            session = ClientSession(read, write)

            # ✅ OBLIGATOIRE : handshake MCP
            await session.initialize()

            self._clients[name] = client_cm
            self._sessions[name] = session

            print(f">>> [MCP] Initialized: {name}")

        return self

    async def __aexit__(self, exc_type, exc, tb):
        for session in self._sessions.values():
            try:
                await session.close()
            except Exception:
                pass

        for client_cm in self._clients.values():
            try:
                await client_cm.__aexit__(None, None, None)
            except Exception:
                pass

        self._sessions.clear()
        self._clients.clear()

    async def list_tools(self) -> Tuple[Dict[str, str], Dict[str, ClientSession]]:
        catalog: Dict[str, str] = {}
        mapping: Dict[str, ClientSession] = {}

        for server_name, session in self._sessions.items():
            tools = await session.list_tools()
            for tool in tools:
                full = f"{server_name}.{tool.name}"
                catalog[full] = tool.description or ""
                mapping[full] = session

        return catalog, mapping

    async def call_tool(self, tool_name: str, args: dict, mapping: Dict[str, ClientSession]):
        session = mapping[tool_name]
        short = tool_name.split(".", 1)[1]
        return await session.call_tool(short, args)
