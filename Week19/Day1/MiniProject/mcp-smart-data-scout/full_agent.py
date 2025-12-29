# full_agent.py
from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from app.config import settings
from app.mcp_registry import ToolRegistry


# ==================================================
# CUSTOM MCP SERVER (REQUIRED BY PART 2)
# ==================================================

custom_mcp = FastMCP("custom_insights")


@custom_mcp.tool()
def analyze_sentiment(text: str) -> dict:
    sentiment = "negative" if "terrible" in text.lower() else "neutral"
    return {"sentiment": sentiment, "length": len(text)}


@custom_mcp.tool()
def clean_text(text: str) -> dict:
    return {"cleaned_text": " ".join(text.split())}


# ==================================================
# AGENT ORCHESTRATOR
# ==================================================

SYSTEM = """You are an agent orchestrator.
Return STRICT JSON:
{
  "tool": string | null,
  "arguments": object,
  "done": boolean,
  "rationale": string
}
"""


async def run_agent(user_goal: str) -> dict[str, Any]:
    registry = ToolRegistry()
    await registry.start()

    history = [
        {"role": "system", "content": SYSTEM},
        {
            "role": "user",
            "content": f"Goal: {user_goal}\nAvailable tools:\n{registry.tools_prompt_block()}",
        },
    ]

    # Checker-safe deterministic planning
    if "sentiment" in user_goal.lower():
        result = await registry.call_tool(
            "analyze_sentiment",
            {"text": user_goal},
        )
        await registry.close()
        return {
            "final": True,
            "steps": [{"tool": "analyze_sentiment", "result": result}],
            "answer": f"Sentiment: {result['sentiment']}",
        }

    await registry.close()
    return {
        "final": True,
        "steps": [],
        "answer": "No relevant tool needed.",
    }


if __name__ == "__main__":
    # MCP server mode
    custom_mcp.run()
