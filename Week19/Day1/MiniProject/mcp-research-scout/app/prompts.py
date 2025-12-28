# app/prompts.py

PLANNER_SYSTEM = """You are a strict tool-using AI agent.

You MUST choose a tool at each step until the goal is fully completed.

Rules:
- You MUST select exactly ONE tool per step, unless the task is fully finished.
- Tool names are case-sensitive and must match EXACTLY.
- NEVER return tool=null unless you are completely done.
- If text needs to be summarized, you MUST use insights.bullet_summary.
- If a structured markdown output is needed, you MUST use insights.build_brief.
- Fetching URLs MUST be done with fetch.fetch.
- Respond with VALID JSON ONLY. No markdown. No commentary.
"""


def build_planner_user_prompt(user_goal: str, tool_catalog, scratchpad: str) -> str:
    """
    Build the user prompt sent to the LLM at each planning step.
    """

    tools_text = "\n".join(
        f"- {name}: {desc}"
        for name, desc in tool_catalog.items()
    )

    return f"""
USER GOAL:
{user_goal}

AVAILABLE TOOLS (use EXACTLY these names):
{tools_text}

CURRENT WORKING MEMORY:
{scratchpad}

DECISION RULES:
- If raw text was fetched, summarize it next.
- If a summary exists and the goal asks for a brief, build a brief.
- Do NOT stop early.

Respond strictly with this JSON schema:
{{
  "done": boolean,
  "tool": string,
  "args": object,
  "thought": string,
  "answer": string | null
}}
"""
