# app/mcp_registry.py
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List

from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

from app.config import settings


# ==============================
# Errors
# ==============================

class ToolRegistryError(RuntimeError):
    pass


# ==============================
# Tool metadata
# ==============================

@dataclass
class ToolInfo:
    name: str
    description: str | None = None
    input_schema: dict[str, Any] | None = None


# ==============================
# Registry
# ==============================

class ToolRegistry:
    """
    Starts MCP servers, discovers tools, and dispatches tool calls.
    Robust against server startup failures (timeouts).
    """

    def __init__(self) -> None:
        self.sessions: Dict[str, ClientSession] = {}
        self._contexts: List[Any] = []
        self._tools_cache: List[ToolInfo] = []

    # ==============================
    # Lifecycle
    # ==============================

    async def start(self) -> None:
        print("[MCP] Registry starting")

        await self._connect(
            "time",
            settings.mcp_time_command,
            settings.mcp_time_args,
        )

        await self._connect(
            "fetch",
            settings.mcp_fetch_command,
            settings.mcp_fetch_args,
        )

        await self._connect(
            "insights",
            settings.mcp_insights_command,
            settings.mcp_insights_args,
        )

        await self.discover_tools()
        print("[MCP] Registry ready")

    async def close(self) -> None:
        print("[MCP] Registry closing")

        for ctx in reversed(self._contexts):
            try:
                await ctx.__aexit__(None, None, None)
            except Exception:
                pass

        self.sessions.clear()
        self._contexts.clear()
        self._tools_cache.clear()

        print("[MCP] Registry closed")

    # ==============================
    # Connections (SAFE, TIMEOUT)
    # ==============================

    async def _connect(self, name: str, command: str, args: list[str]) -> None:
        print(f"[MCP] Starting '{name}' server...")

        params = StdioServerParameters(command=command, args=args)
        ctx = stdio_client(params)
        self._contexts.append(ctx)

        async def _enter_ctx():
            return await ctx.__aenter__()

        task = asyncio.create_task(_enter_ctx())

        try:
            # ⬅️ TIMEOUT CRITIQUE (sinon freeze)
            read, write = await asyncio.wait_for(task, timeout=5.0)
        except asyncio.TimeoutError:
            print(f"[MCP] ⚠️ '{name}' did not respond (timeout), skipped")
            task.cancel()
            return
        except Exception as e:
            print(f"[MCP] ❌ '{name}' failed to start: {e}")
            task.cancel()
            return

        session = ClientSession(read, write)

        try:
            # ⬅️ INITIALIZE PEUT BLOQUER AUSSI → timeout
            await asyncio.wait_for(session.initialize(), timeout=5.0)
        except asyncio.TimeoutError:
            print(f"[MCP] ⚠️ '{name}' initialize timeout, skipped")
            return
        except Exception as e:
            print(f"[MCP] ❌ '{name}' initialize failed: {e}")
            return

        self.sessions[name] = session
        print(f"[MCP] Connected to '{name}'")

    # ==============================
    # Tool discovery
    # ==============================

    async def discover_tools(self) -> List[ToolInfo]:
        """
        Query all connected servers and cache tool metadata.
        """
        tools: List[ToolInfo] = []

        for server_name, session in self.sessions.items():
            try:
                resp = await asyncio.wait_for(session.list_tools(), timeout=5.0)
            except Exception as e:
                print(f"[MCP] ⚠️ Failed to list tools from '{server_name}': {e}")
                continue

            for t in resp.tools:
                tools.append(
                    ToolInfo(
                        name=str(t.name),
                        description=getattr(t, "description", None),
                        input_schema=getattr(t, "inputSchema", None),
                    )
                )

        self._tools_cache = tools
        print(f"[MCP] Discovered {len(tools)} tools")
        return tools

    def tools_prompt_block(self) -> str:
        """
        Human-readable block for LLM prompt.
        """
        if not self._tools_cache:
            return "(no tools available)"

        lines: List[str] = []

        for t in self._tools_cache:
            line = f"- {t.name}"
            if t.description:
                line += f": {t.description.strip()}"
            lines.append(line)

            if t.input_schema:
                lines.append(f"  input_schema: {t.input_schema}")

        return "\n".join(lines)

    # ==============================
    # Tool execution
    # ==============================

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call a tool on whichever server provides it.
        Retries on failure.
        """
        last_err: Exception | None = None

        for attempt in range(settings.max_retries + 1):
            for session in self.sessions.values():
                try:
                    res = await asyncio.wait_for(
                        session.call_tool(tool_name, arguments),
                        timeout=8.0,
                    )
                    return res.content
                except Exception as e:
                    last_err = e
                    continue

            if attempt < settings.max_retries:
                await asyncio.sleep(0.5 * (attempt + 1))

        raise ToolRegistryError(
            f"Tool '{tool_name}' failed after retries: {last_err}"
        )
