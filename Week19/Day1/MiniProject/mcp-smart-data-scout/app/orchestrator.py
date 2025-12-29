# app/orchestrator.py
import asyncio
from app.llm_client import call_llm
from app.logging_utils import log_tool_call

class Orchestrator:
    def __init__(self, registry):
        self.registry = registry

    async def run(self, question: str) -> str:
        # Ask LLM what to do
        decision = call_llm([
            {"role": "system", "content": "Choose one tool: time, fetch, insights"},
            {"role": "user", "content": question},
        ])

        result_parts = []

        try:
            if "time" in decision.lower():
                res = await self.registry.call("time", "now", None)
                log_tool_call("time.now", None, res)
                result_parts.append(str(res))

            if "fetch" in decision.lower():
                res = await self.registry.call(
                    "fetch",
                    "fetch",
                    {"url": "https://example.com"}
                )
                log_tool_call("fetch.fetch", {"url": "https://example.com"}, res)
                result_parts.append("Fetched example.com")

            # Always run insights (custom server)
            res = await self.registry.call(
                "insights",
                "analyze",
                {"text": question}
            )
            log_tool_call("insights.analyze", {"text": question}, res)
            result_parts.append(str(res))

        except Exception as e:
            result_parts.append(f"Error: {e}")

        return "\n".join(result_parts)
