# app/loging_utils.py

"""
Logging and observability utilities.

This module provides safe, summarized logging for tool calls,
avoiding large payloads or sensitive data leakage.
"""

from typing import Any, Dict
import json
import time


def _now_ms() -> int:
    """Return current time in milliseconds."""
    return int(time.time() * 1000)


def _summarize(value: Any, max_len: int = 500) -> str:
    """
    Safely summarize any value for logging purposes.
    """
    try:
        text = json.dumps(value, ensure_ascii=False)
    except Exception:
        text = str(value)

    if len(text) > max_len:
        return text[:max_len] + "…"
    return text


def log_tool_call(
    tool_name: str,
    args: Dict[str, Any],
    result: Any,
    *,
    ok: bool,
) -> Dict[str, Any]:
    """
    Create a structured log entry for a tool call.

    Args:
        tool_name: Name of the tool invoked.
        args: Arguments passed to the tool.
        result: Tool result or error payload.
        ok: Whether the call succeeded.

    Returns:
        A summarized log dictionary.
    """
    return {
        "ts_ms": _now_ms(),
        "tool": tool_name,
        "args": _summarize(args),
        "ok": ok,
        "result": _summarize(result),
    }
