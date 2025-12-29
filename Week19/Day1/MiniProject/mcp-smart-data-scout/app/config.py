"""
Application configuration (validated & MCP-safe)

- LLM backend (Groq / Ollama)
- MCP stdio servers (time, fetch)
- Agent limits
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    # ======================================================
    # LLM BACKEND
    # ======================================================

    llm_backend: str = Field(
        default="groq",
        description="LLM backend: groq or ollama",
    )

    # ---- Groq ----
    groq_api_key: str | None = Field(default=None)
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_model: str = "llama-3.1-70b-versatile"

    # ---- Ollama ----
    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_model: str = "llama3"

    # ======================================================
    # MCP SERVERS (STDIO)
    # ======================================================

    # ---- TIME (third-party) ----
    mcp_time_command: str = "python"
    mcp_time_args: str = "-m,mcp_server_time,--local-timezone,UTC"

    # ---- FETCH (third-party) ----
    mcp_fetch_command: str = "python"
    mcp_fetch_args: str = "-m,mcp_server_fetch"

    # ======================================================
    # AGENT LIMITS
    # ======================================================

    max_steps: int = 8
    max_retries: int = 2

    # ======================================================
    # SETTINGS META
    # ======================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",   # 🔴 IMPORTANT: prevents crash on extra env vars
    )

    # ======================================================
    # VALIDATORS
    # ======================================================

    @field_validator("llm_backend")
    @classmethod
    def validate_backend(cls, v: str) -> str:
        v = v.lower()
        if v not in {"groq", "ollama"}:
            raise ValueError("llm_backend must be 'groq' or 'ollama'")
        return v

    @field_validator("groq_api_key")
    @classmethod
    def validate_groq_key(cls, v, info):
        if info.data.get("llm_backend") == "groq" and not v:
            raise ValueError("GROQ_API_KEY must be set when using Groq")
        return v

    # ======================================================
    # HELPERS
    # ======================================================

    @property
    def active_llm_base_url(self) -> str:
        return self.groq_base_url if self.llm_backend == "groq" else self.ollama_base_url

    @property
    def active_llm_model(self) -> str:
        return self.groq_model if self.llm_backend == "groq" else self.ollama_model

    @property
    def mcp_time_args_list(self) -> list[str]:
        return [a.strip() for a in self.mcp_time_args.split(",")]

    @property
    def mcp_fetch_args_list(self) -> list[str]:
        return [a.strip() for a in self.mcp_fetch_args.split(",")]


# Singleton
settings = Settings()
