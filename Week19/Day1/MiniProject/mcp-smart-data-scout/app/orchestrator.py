# app/orchestrator.py

"""
Agentic Orchestrator.

Responsibilities:
- Take a user goal
- Ask the LLM to plan tool usage
- Execute steps iteratively
- Respect MAX_STEPS
- Log actions and outcomes

This orchestrator is backend-agnostic (Groq or Ollama).
"""

from typing import Dict, Any, List

from app.config import settings
from app.llm_client import call_llm
from app.mcp_registry import ToolRegistry
from app.logging_utils import log_tool_call


class Orchestrator:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        self.max_steps = settings.max_steps
        self.logs: List[Dict[str, Any]] = []

    # ==============================
    # Public API
    # ==============================

    def run(self, user_goal: str) -> str:
        """
        Run an agentic loop to achieve the user goal.
        """
        tools = self.registry.list_tools()
        context: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": (
                    "You are an AI agent that can use tools to achieve a goal.\n"
                    "You must choose the most appropriate tool and arguments.\n"
                    "If no tool is needed, answer directly.\n"
                    "Respond in JSON with the following format:\n"
                    "{\n"
                    '  "action": "tool" | "final",\n'
                    '  "tool_name": string | null,\n'
                    '  "arguments": object | null,\n'
                    '  "final_answer": string | null\n'
                    "}"
                ),
            },
            {
                "role": "user",
                "content": f"Goal: {user_goal}\n\nAvailable tools:\n{tools}",
            },
        ]

        for step in range(1, self.max_steps + 1):
            response = call_llm(context)
            decision = self._parse_llm_response(response)

            if decision["action"] == "final":
                return decision["final_answer"]

            if decision["action"] == "tool":
                result = self._execute_tool(
                    decision["tool_name"],
                    decision["arguments"] or {},
                )

                return (
                    f"I used the tool `{decision['tool_name']}` to answer your question.\n\n"
                    f"{result}"
                )

            raise RuntimeError("Invalid LLM action")

        return "Stopped: maximum number of steps reached."

    # ==============================
    # Internals
    # ==============================

    def _execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Simulate tool execution for the mini-project.

        The goal here is to demonstrate correct tool selection
        and orchestration logic, not low-level MCP execution.
        """
        if tool_name == "time.now":
            return "The current time can be retrieved using the time.now tool."

        if tool_name == "fetch.fetch":
            return "Web content can be fetched using the fetch.fetch tool."

        return f"Tool {tool_name} executed with arguments {arguments}"

    def _parse_llm_response(self, text: str) -> Dict[str, Any]:
        """
        Parse the JSON response from the LLM safely.
        """
        import json

        try:
            return json.loads(text)
        except Exception:
            return {
                "action": "final",
                "tool_name": None,
                "arguments": None,
                "final_answer": text,
            }
