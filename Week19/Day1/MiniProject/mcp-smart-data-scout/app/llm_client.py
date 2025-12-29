# app/llm_client.py
from __future__ import annotations

import time
import requests

from app.config import settings


class LLMError(RuntimeError):
    pass


def call_llm(messages: list[dict[str, str]], temperature: float = 0.2) -> str:
    url = f"{settings.active_llm_base_url}/chat/completions"

    headers = {"Content-Type": "application/json"}
    if settings.llm_backend.lower() == "groq":
        if not settings.groq_api_key:
            raise LLMError("GROQ_API_KEY missing")
        headers["Authorization"] = f"Bearer {settings.groq_api_key}"

    payload = {
        "model": settings.active_llm_model,
        "messages": messages,
        "temperature": temperature,
    }

    last_err = None
    for attempt in range(settings.max_retries + 1):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=30)
            if r.status_code >= 400:
                raise LLMError(r.text[:300])
            return r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            last_err = e
            time.sleep(0.5 * (attempt + 1))

    raise LLMError(f"LLM failed: {last_err}")
