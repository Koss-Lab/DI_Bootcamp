# app/llm_client.py
import requests
import time
from app.config import settings


def call_llm(messages, temperature: float = 0.2) -> str:
    # 🔥 FALLBACK ABSOLU : si pas de clé → réponse déterministe
    if settings.llm_backend == "groq" and not settings.groq_api_key:
        return """
{
  "tool": "time.now",
  "arguments": {},
  "done": false,
  "rationale": "Need current time"
}
""".strip()

    url = f"{settings.active_llm_base_url}/chat/completions"
    headers = {"Content-Type": "application/json"}

    if settings.llm_backend == "groq":
        headers["Authorization"] = f"Bearer {settings.groq_api_key}"

    payload = {
        "model": settings.active_llm_model,
        "messages": messages,
        "temperature": temperature,
    }

    for attempt in range(settings.max_retries + 1):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=20)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception:
            time.sleep(0.4)

    # 🔥 ULTIME FILET DE SÉCURITÉ
    return """
{
  "tool": null,
  "arguments": {},
  "done": true,
  "rationale": "Fallback answer"
}
""".strip()
