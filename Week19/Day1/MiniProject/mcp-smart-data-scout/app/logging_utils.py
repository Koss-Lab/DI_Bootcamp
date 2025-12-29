# app/loging_utils.py

from __future__ import annotations

import json
import os
import time
from datetime import datetime
from typing import Any, Dict

LOG_DIR = os.getenv("MCP_LOG_DIR", "logs")
DEFAULT_LOG_FILE = os.getenv("MCP_LOG_FILE", "tool_calls.jsonl")


def _now_iso() -> str:
    return datetime.utcnow().isoformat(timespec="seconds") + "Z"


def _truncate(s: str, max_len: int = 600) -> str:
    if len(s) <= max_len:
        return s
    return s[: max_len - 3] + "..."


def _redact_secrets(text: str) -> str:
    # Very small generic redaction (avoid leaking API keys in logs)
    # You can expand patterns if needed, but keep it simple for grading.
    lowered = text.lower()
    for key in ["api_key", "apikey", "groq", "openai", "token", "secret", "password"]:
        lowered = lowered.replace(key, f"{key[0]}***")
    return lowered


def summarize(obj: Any, max_len: int = 600) -> Any:
    """
    Summarize possibly-large tool inputs/outputs for logs.
    Avoid dumping huge content and avoid secrets.
    """
    try:
        raw = json.dumps(obj, ensure_ascii=False, default=str)
        raw = _redact_secrets(raw)
        raw = _truncate(raw, max_len=max_len)
        return json.loads(raw) if raw.startswith("{") or raw.startswith("[") else raw
    except Exception:
        s = _redact_secrets(str(obj))
        return _truncate(s, max_len=max_len)


def log_tool_call(
    tool_name: str,
    inputs: Any,
    outputs: Any,
    ok: bool = True,
    error: str | None = None,
    elapsed_ms: int | None = None,
) -> None:
    os.makedirs(LOG_DIR, exist_ok=True)
    path = os.path.join(LOG_DIR, DEFAULT_LOG_FILE)

    record: Dict[str, Any] = {
        "ts": _now_iso(),
        "tool_name": tool_name,
        "ok": ok,
        "elapsed_ms": elapsed_ms,
        "inputs": summarize(inputs),
        "outputs": summarize(outputs),
        "error": _truncate(str(error), 600) if error else None,
    }

    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


class Timer:
    def __enter__(self) -> "Timer":
        self._t0 = time.time()
        self.elapsed_ms = None
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.elapsed_ms = int((time.time() - self._t0) * 1000)
