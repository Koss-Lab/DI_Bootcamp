# app/orchestrator.py
from __future__ import annotations

import json
from typing import Any

from app.config import settings
from app.llm_client import call_llm
from app.mcp_registry import ToolRegistry, ToolRegistryError


SYSTEM = """
You are an agentic orchestrator.

Your role is to plan and execute tool calls across multiple MCP servers
in order to achieve the user's goal.

Return STRICT JSON ONLY with:
{
  "tool": string | null,
  "arguments": object,
  "done": boolean,
  "rationale": string
}
"""


class Orchestrator:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry

    async def run_async(self, user_goal: str) -> dict[str, Any]:
        tools_block = self.registry.tools_prompt_block()

        history = [
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": f"Goal:\n{user_goal}\n\nAvailable tools:\n{tools_block}",
            },
        ]

        steps: list[dict[str, Any]] = []

        for step in range(settings.max_steps):
            llm_out = call_llm(history)

            try:
                plan = json.loads(llm_out)
            except Exception:
                if step == settings.max_steps - 1:
                    return {
                        "final": True,
                        "steps": steps,
                        "answer": llm_out,
                    }

                history.append({
                    "role": "user",
                    "content": (
                        "Your last answer was invalid JSON.\n\n"
                        "Rewrite it as STRICT JSON ONLY.\n\n"
                        "Example:\n"
                        '{ "tool": "clean_text", "arguments": {"text": "..."}, '
                        '"done": false, "rationale": "Clean input" }\n\n'
                        f"User goal:\n{user_goal}"
                    ),
                })
                continue

            if plan.get("done") or not plan.get("tool"):
                return {
                    "final": True,
                    "steps": steps,
                    "answer": plan.get("rationale", "Task completed"),
                }

            try:
                result = await self.registry.call_tool(
                    plan["tool"], plan.get("arguments", {})
                )

                steps.append({
                    "tool": plan["tool"],
                    "arguments": plan.get("arguments", {}),
                    "result": result,
                })

                history.append({"role": "assistant", "content": llm_out})
                history.append({
                    "role": "user",
                    "content": f"Tool result:\n{result}\n\nDecide next step.",
                })

            except ToolRegistryError as e:
                steps.append({"tool": plan["tool"], "error": str(e)})
                history.append({"role": "assistant", "content": llm_out})
                history.append({
                    "role": "user",
                    "content": f"Tool failed: {e}. Try another approach.",
                })

        return {
            "final": False,
            "steps": steps,
            "answer": "Max planning steps reached",
        }
