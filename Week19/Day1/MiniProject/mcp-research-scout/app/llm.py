# app/llm.py

import os
import json
import requests
from typing import Any, Dict, Optional

from groq import Groq


def _safe_json_parse(text: str) -> Dict[str, Any]:
    """
    Parse JSON safely from model output.
    Removes markdown fences if the model adds them.
    """
    text = text.strip()

    if text.startswith("```"):
        text = text.split("```", 2)[1].strip()

    return json.loads(text)


class LLMClient:
    """
    Unified LLM client.
    - Uses Groq if GROQ_API_KEY is set
    - Falls back to Ollama otherwise
    """

    def __init__(self) -> None:
        self.groq_api_key = os.getenv("GROQ_API_KEY", "").strip()
        self.groq_model = os.getenv("GROQ_MODEL", "llama3-70b-8192")

        self.ollama_base_url = os.getenv(
            "OLLAMA_BASE_URL", "http://localhost:11434"
        )
        self.ollama_model = os.getenv("OLLAMA_MODEL", "llama3.1")

        self._groq_client: Optional[Groq] = None

        if self.groq_api_key:
            self._groq_client = Groq(api_key=self.groq_api_key)

    def plan(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """
        Ask the LLM to choose the next tool and arguments.
        Must return valid JSON.
        """
        if self._groq_client:
            response = self._groq_client.chat.completions.create(
                model=self.groq_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
            )

            content = response.choices[0].message.content or "{}"
            return _safe_json_parse(content)

        # --- Ollama fallback (OpenAI-compatible endpoint) ---
        url = f"{self.ollama_base_url}/v1/chat/completions"

        payload = {
            "model": self.ollama_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        }

        r = requests.post(url, json=payload, timeout=60)
        r.raise_for_status()

        data = r.json()
        content = (
            data.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "{}")
        )

        return _safe_json_parse(content)
