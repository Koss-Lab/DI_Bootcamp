# app/orchestrator.py

from app.config import settings
from app.mcp_registry import ToolRegistry


class Orchestrator:
    """
    LLM-driven planner that selects and executes MCP tools.
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def _llm_plan(self, user_input: str) -> dict:
        """
        Simulated LLM planning step.
        In a real system, this would call Groq or Ollama.
        """

        print("[LLM] Planning next tool call...")

        text = user_input.lower()

        if "time" in text:
            return {"tool": "time.now", "args": {}}

        if "analyze" in text:
            return {
                "tool": "insights.analyze",
                "args": {"text": user_input.replace("Analyze:", "").strip()},
            }

        return {
            "tool": "fetch.fetch",
            "args": {"url": "https://example.com"},
        }

    async def run_async(self, user_input: str):
        context = []
        steps = 0

        while steps < settings.max_steps:
            plan = self._llm_plan(user_input)

            tool = plan["tool"]
            args = plan["args"]

            try:
                result = await self.registry.call_tool(tool, args)
                context.append({"tool": tool, "result": result})
                return {
                    "tool": tool,
                    "result": result,
                }

            except Exception as e:
                print(f"[ERROR] Tool failed: {e}")
                steps += 1

                if steps >= settings.max_retries:
                    return {"error": str(e)}

        return {"error": "Max steps exceeded"}
