# app/llm_client.py

from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.config import settings


class LLMError(RuntimeError):
    pass


@dataclass
class LLMResponse:
    text: str
    raw: Dict[str, Any]


def _auth_headers() -> Dict[str, str]:
    # GroqCloud: uses OpenAI-compatible Bearer token header
    # Ollama: no auth by default
    if settings.llm_backend.lower() == "groq":
        if not settings.groq_api_key:
            raise LLMError("Missing GROQ_API_KEY in environment (.env).")
        return {"Authorization": f"Bearer {settings.groq_api_key}"}
    return {}


def _validate_messages(messages: List[Dict[str, str]]) -> None:
    if not isinstance(messages, list) or not messages:
        raise LLMError("messages must be a non-empty list.")
    for i, m in enumerate(messages):
        if not isinstance(m, dict):
            raise LLMError(f"messages[{i}] must be a dict.")
        if "role" not in m or "content" not in m:
            raise LLMError(f"messages[{i}] must contain 'role' and 'content'.")
        if m["role"] not in ("system", "user", "assistant", "tool"):
            raise LLMError(f"messages[{i}].role invalid: {m['role']}")
        if not isinstance(m["content"], str):
            raise LLMError(f"messages[{i}].content must be a string.")


def _payload(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    _validate_messages(messages)
    # OpenAI-like schema
    return {
        "model": settings.active_llm_model,
        "messages": messages,
        "temperature": settings.temperature,
        "max_tokens": settings.max_tokens,
    }


def _parse_chat_completion(resp_json: Dict[str, Any]) -> str:
    try:
        return resp_json["choices"][0]["message"]["content"]
    except Exception as e:
        raise LLMError(f"Unexpected LLM response format: {e}. Raw={str(resp_json)[:400]}")


@retry(
    stop=stop_after_attempt(lambda: settings.max_retries),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type((requests.RequestException, LLMError)),
    reraise=True,
)
def call_llm(messages: List[Dict[str, str]]) -> str:
    url = settings.active_llm_base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Content-Type": "application/json",
        **_auth_headers(),
    }

    # Jitter (avoid synchronized retries)
    if settings.max_retries > 1:
        jitter = random.random() * 0.2
    else:
        jitter = 0.0

    try:
        resp = requests.post(
            url,
            headers=headers,
            data=json.dumps(_payload(messages)),
            timeout=settings.http_timeout_sec + jitter,
        )
    except requests.RequestException as e:
        raise LLMError(f"LLM network error: {e}") from e

    if resp.status_code >= 400:
        # Keep it short
        raise LLMError(f"LLM HTTP {resp.status_code}: {resp.text[:400]}")

    try:
        data = resp.json()
    except Exception as e:
        raise LLMError(f"LLM returned non-JSON response: {e}. Body={resp.text[:300]}") from e

    return _parse_chat_completion(data)
