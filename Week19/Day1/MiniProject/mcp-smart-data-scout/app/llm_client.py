# app/llm_client.py

"""
LLM HTTP client.

This module provides a unified interface to call either:
- GroqCloud (hosted) via OpenAI-compatible REST API
- Ollama (local) via OpenAI-compatible REST API

Backend selection and endpoints are fully environment-based.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.config import settings


class LLMError(RuntimeError):
    """Raised when the LLM call fails."""


def _auth_headers() -> Dict[str, str]:
    """
    Build authorization headers depending on the active backend.
    """
    headers = {
        "Content-Type": "application/json",
    }
    if settings.is_groq:
        headers["Authorization"] = f"Bearer {settings.groq_api_key}"
    # Ollama does not require auth headers
    return headers


def _endpoint() -> str:
    """
    Chat Completions endpoint (OpenAI-compatible).
    """
    base = settings.active_llm_base_url.rstrip("/")
    return f"{base}/chat/completions"


def _payload(
    messages: List[Dict[str, str]],
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Build the request payload.
    """
    data: Dict[str, Any] = {
        "model": settings.active_llm_model,
        "messages": messages,
        "temperature": temperature,
    }
    if max_tokens is not None:
        data["max_tokens"] = max_tokens
    return data


@retry(
    reraise=True,
    stop=stop_after_attempt(settings.max_retries + 1),
    wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
    retry=retry_if_exception_type((httpx.TimeoutException, httpx.NetworkError)),
)
def call_llm(
    messages: List[Dict[str, str]],
    *,
    temperature: float = 0.2,
    max_tokens: Optional[int] = None,
    timeout_s: float = 30.0,
) -> str:
    """
    Call the configured LLM backend and return the assistant text.

    Args:
        messages: OpenAI-style chat messages.
        temperature: Sampling temperature.
        max_tokens: Optional output token limit.
        timeout_s: Request timeout in seconds.

    Returns:
        Assistant message content as string.

    Raises:
        LLMError: On HTTP or response parsing errors.
    """
    url = _endpoint()
    headers = _auth_headers()
    data = _payload(messages, temperature=temperature, max_tokens=max_tokens)

    try:
        with httpx.Client(timeout=timeout_s) as client:
            resp = client.post(url, headers=headers, json=data)
    except httpx.TimeoutException as e:
        raise LLMError(f"LLM request timed out: {e}") from e
    except httpx.NetworkError as e:
        raise LLMError(f"LLM network error: {e}") from e

    if resp.status_code != 200:
        raise LLMError(
            f"LLM HTTP {resp.status_code}: {resp.text[:300]}"
        )

    try:
        payload = resp.json()
        choices = payload.get("choices", [])
        if not choices:
            raise KeyError("choices")
        message = choices[0].get("message", {})
        content = message.get("content")
        if not content:
            raise KeyError("message.content")
        return content
    except Exception as e:
        raise LLMError(f"Invalid LLM response format: {e}") from e
