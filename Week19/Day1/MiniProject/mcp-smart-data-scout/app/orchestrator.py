# app/orchestrator.py

import asyncio
import json
from app.llm_client import call_llm


class Orchestrator:
    """
    Async-safe LLM-driven orchestrator.
    """

    def __init__(self, registry):
        self.registry = registry

    async def run_async(self, user_input: str) -> str:
        # 1. Ask LLM (RUN IN THREAD)
        plan = await asyncio.to_thread(
            call_llm,
            [
                {
                    "role": "system",
                    "content": (
                        "You are an agent that selects the best MCP tool.\n"
                        "Reply ONLY in JSON:\n"
                        "{ \"tool\": \"tool.name\", \"args\": { ... } }\n"
                        "Available tools:\n"
                        f"{', '.join(self.registry.list_tools())}"
                    ),
                },
                {"role": "user", "content": user_input},
            ],
        )

        # 2. Parse JSON
        try:
            decision = json.loads(plan)
            tool_name = decision["tool"]
            args = decision.get("args", {})
        except Exception:
            return f"LLM planning error:\n{plan}"

        # 3. Execute MCP tool
        try:
            result = await self.registry.call_tool(tool_name, args)
        except Exception as e:
            return f"Tool execution error: {e}"

        # 4. RETURN RESULT
        return str(result)
