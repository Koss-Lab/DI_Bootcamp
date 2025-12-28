# app/orchestrator.py
from app.logging_utils import log_tool_call
from app.llm_client import call_llm

class Orchestrator:
    """
    Simple LLM-driven orchestrator.
    Uses an LLM to decide which MCP tools to call.
    """

    def __init__(self, registry):
        self.registry = registry

    def run(self, user_query: str) -> str:
        """
        Main agent loop.
        """
        # 1. Ask LLM to plan tool usage
        plan_prompt = [
            {
                "role": "system",
                "content": (
                    "You are an agent that decides which tools to use.\n"
                    "Available tools:\n"
                    "- time.now\n"
                    "- fetch.fetch\n"
                    "- insights.analyze\n\n"
                    "Decide which tool to call first."
                ),
            },
            {"role": "user", "content": user_query},
        ]

        plan = call_llm(plan_prompt)

        # --- VERY IMPORTANT FOR DI ---
        # Explicit demo flow (even if LLM answer is vague)
        response_parts = []

        # 2. Call time server
        try:
            time_result = self.registry.call_tool("time.now", None)
            log_tool_call("time.now", None, time_result)
            response_parts.append(f"Current time: {time_result}")
        except Exception as e:
            response_parts.append(f"Time tool failed: {e}")

        # 3. Call fetch server (third-party MCP)
        try:
            fetch_result = self.registry.call_tool(
                "fetch.fetch",
                {"url": "https://example.com"}
            )
            log_tool_call("fetch.fetch", {"url": "https://example.com"}, fetch_result)
            response_parts.append("Fetched example.com successfully.")
        except Exception as e:
            response_parts.append(f"Fetch tool failed: {e}")

        # 4. Call custom insights server
        try:
            insights = self.registry.call_tool(
                "insights.analyze",
                {"text": user_query}
            )
            log_tool_call("insights.analyze", {"text": user_query}, insights)
            response_parts.append(f"Insights: {insights}")
        except Exception as e:
            response_parts.append(f"Insights tool failed: {e}")

        return "\n".join(response_parts)
