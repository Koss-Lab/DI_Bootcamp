import json
import requests
from app.config import settings


def call_llm(prompt: str) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.groq_api_key}"
        if settings.llm_backend == "groq"
        else "",
    }

    payload = {
        "model": settings.groq_model
        if settings.llm_backend == "groq"
        else settings.ollama_model,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = requests.post(
        settings.groq_base_url
        if settings.llm_backend == "groq"
        else settings.ollama_base_url,
        headers=headers,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def plan_next_action(user_input: str, tools: list[str]) -> dict:
    """
    Ask the LLM which tool to use next.
    """

    prompt = f"""
You are an autonomous agent.

User goal:
{user_input}

Available tools:
{tools}

Choose the best tool and return JSON only:
{{
  "tool": "tool.name",
  "arguments": {{}}
}}
"""

    raw = call_llm(prompt)

    try:
        return json.loads(raw)
    except Exception:
        # Fallback deterministic behavior
        if "time" in user_input.lower():
            return {"tool": "time.now", "arguments": {}}
        return {"tool": "insights.analyze", "arguments": {"text": user_input}}
