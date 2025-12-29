# app/orchestrator.py
import json
from app.llm_client import call_llm
from app.config import settings


SYSTEM = """You are an agent orchestrator.
Return STRICT JSON only:
{
  "tool": string | null,
  "arguments": object,
  "done": boolean,
  "rationale": string
}
"""


class Orchestrator:
    def __init__(self, registry):
        self.registry = registry

    async def run_async(self, user_goal: str):
        history = [
            {"role": "system", "content": SYSTEM},
            {
                "role": "user",
                "content": f"Goal: {user_goal}\n\nAvailable tools:\n{self.registry.tools_prompt_block()}",
            },
        ]

        steps = []

        for step in range(settings.max_steps):
            llm_out = call_llm(history)

            try:
                plan = json.loads(llm_out)
            except Exception:
                # 🔥 FIX DÉFINITIF : FORCER JSON
                history.append({
                    "role": "user",
                    "content": f"""
Rewrite STRICT JSON ONLY.

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

            tool = plan.get("tool")
            args = plan.get("arguments", {})
            done = plan.get("done", False)

            if done or not tool:
                return {
                    "final": True,
                    "steps": steps,
                    "answer": plan.get("rationale", "Done"),
                }

            result = await self.registry.call_tool(tool, args)
            steps.append({"tool": tool, "args": args, "result": result})

            history.append({"role": "assistant", "content": llm_out})
            history.append({
                "role": "user",
                "content": f"Tool result: {result}. Decide next step.",
            })

        # 🔥 FALLBACK ULTIME
        return {
            "final": True,
            "steps": steps,
            "answer": "Completed with fallback",
        }
