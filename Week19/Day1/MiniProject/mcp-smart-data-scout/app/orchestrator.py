# app/orchestrator.py

from app.config import settings
from app.mcp_registry import ToolRegistry


class Orchestrator:
    """
    Minimal, reliable agent orchestrator.
    Guaranteed to RETURN output (never None).
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    async def run_async(self, user_input: str):
        """
        Main agent entry point.
        ALWAYS returns a value.
        """

        user_input = user_input.strip()

        # ----------------------------
        # TIME QUERY
        # ----------------------------
        if "time" in user_input.lower():
            result = await self.registry.call_tool(
                "time.now",
                {}
            )
            return {
                "tool": "time.now",
                "result": result,
            }

        # ----------------------------
        # ANALYSIS QUERY
        # ----------------------------
        if user_input.lower().startswith("analyze"):
            text = user_input.split(":", 1)[-1].strip()

            result = await self.registry.call_tool(
                "insights.analyze",
                {"text": text}
            )
            return {
                "tool": "insights.analyze",
                "input": text,
                "result": result,
            }

        # ----------------------------
        # FALLBACK
        # ----------------------------
        return {
            "message": "No tool selected",
            "input": user_input,
        }
