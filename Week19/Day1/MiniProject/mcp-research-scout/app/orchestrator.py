# app/orchestrator.py

import asyncio
from typing import Any, Dict, List, Tuple
import os

from app.llm import LLMClient
from app.mcp_multi import MultiMCP
from app.prompts import PLANNER_SYSTEM, build_planner_user_prompt


def _short(obj: Any, limit: int = 500) -> str:
    text = str(obj)
    return text if len(text) <= limit else text[:limit] + "..."


def run_agent(goal: str, max_steps: int = 6) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Runs an MCP-powered agent loop.
    """
    llm = LLMClient()
    logs: List[Dict[str, Any]] = []
    scratchpad = ""

    async def _run() -> str:
        nonlocal scratchpad

        print(">>> [AGENT] Starting MCP context")

        async with MultiMCP() as mcp:
            print(">>> [AGENT] MCP connected, listing tools")

            tools, mapping = await mcp.list_tools()
            logs.append({"event": "tools_loaded", "tools": tools})

            for step in range(1, max_steps + 1):
                print(f">>> [AGENT] Step {step}")
                prompt = build_planner_user_prompt(goal, tools, scratchpad)

                print(">>> [AGENT] Calling LLM planner")
                decision = llm.plan(PLANNER_SYSTEM, prompt)
                print(">>> [AGENT] LLM responded")

                logs.append({"step": step, "plan": decision})

                if decision.get("done"):
                    return decision.get("answer", "Done.")

                tool = decision.get("tool")
                args = decision.get("args") or {}

                if not tool:
                    return "Stopped: no tool selected."

                print(f">>> [AGENT] Calling tool: {tool}")
                result = await mcp.call_tool(tool, args, mapping)
                print(f">>> [AGENT] Tool {tool} finished")

                logs.append(
                    {
                        "step": step,
                        "tool": tool,
                        "args": args,
                        "result": _short(result),
                    }
                )

                scratchpad += (
                    f"\nStep {step}\n"
                    f"Tool: {tool}\n"
                    f"Args: {_short(args)}\n"
                    f"Result: {_short(result)}\n"
                )

                # 🚨 HARD STOP CONDITION (prevents infinite loops)
                if tool == "insights.build_brief":
                    content = result.get("result", "")
                    os.makedirs("workspace", exist_ok=True)
                    path = "workspace/mcp_brief.md"
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(content)

                    logs.append({"event": "file_written", "path": path})
                    return content

            return "Stopped: reached max steps."

    final_answer = asyncio.run(_run())
    return final_answer, logs
