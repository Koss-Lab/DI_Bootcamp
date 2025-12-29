# app/orchestrator.py
from __future__ import annotations

import json
from typing import Any

from app.config import settings
from app.llm_client import call_llm
from app.mcp_registry import ToolRegistry, ToolRegistryError


SYSTEM = """You are an agent orchestrator.
Choose the next MCP tool to call.

Return STRICT JSON only:
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
                "content": f"Goal: {user_goal}\nAvailable tools:\n{tools_block}",
            },
        ]

        steps = []

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
                    "content": f"""
Your last answer was invalid JSON.

Rewrite as STRICT JSON ONLY.

Example:
{{
  "tool": "time.now",
  "arguments": {{}},
  "done": false,
  "rationale": "Need time"
}}

Now answer for:
{user_goal}
"""
                })
                continue

            if plan.get("done") or not plan.get("tool"):
                return {
                    "final": True,
                    "steps": steps,
                    "answer": plan.get("rationale", "Done"),
                }

            try:
                result = await self.registry.call_tool(
                    plan["tool"], plan.get("arguments", {})
                )
                steps.append({
                    "tool": plan["tool"],
                    "args": plan.get("arguments", {}),
                    "result": result,
                })

                history.append({"role": "assistant", "content": llm_out})
                history.append({
                    "role": "user",
                    "content": f"Tool result:\n{result}\nDecide next step.",
                })

            except ToolRegistryError as e:
                steps.append({"tool": plan["tool"], "error": str(e)})
                history.append({"role": "assistant", "content": llm_out})
                history.append({
                    "role": "user",
                    "content": f"Tool failed: {e}. Choose another tool.",
                })

        return {"final": False, "steps": steps, "answer": "Max steps reached"}
