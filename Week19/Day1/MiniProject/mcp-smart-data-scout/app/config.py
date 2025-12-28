# app/config.py

"""
Application configuration.

This module loads and validates all environment-based configuration:
- LLM backend selection (Groq or Ollama)
- LLM endpoints and models
- MCP server settings
- Safety limits for agent execution
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    # ==============================
    # LLM BACKEND CONFIGURATION
    # ==============================

    llm_backend: str = Field(
        default="groq",
        description="LLM backend to use: 'groq' or 'ollama'"
    )

    # --- GroqCloud ---
    groq_api_key: str | None = Field(
        default=None,
        description="Groq API key (required if llm_backend='groq')"
    )
    groq_base_url: str = Field(
        default="https://api.groq.com/openai/v1",
        description="Groq OpenAI-compatible base URL"
    )
    groq_model: str = Field(
        default="llama-3.1-70b-versatile",
        description="Groq model name"
    )

    # --- Ollama (local) ---
    ollama_base_url: str = Field(
        default="http://localhost:11434/v1",
        description="Ollama OpenAI-compatible base URL"
    )
    ollama_model: str = Field(
        default="llama3",
        description="Ollama model name"
    )

    # ==============================
    # MCP SERVERS CONFIGURATION
    # ==============================

    filesystem_allowed_dirs: str = Field(
        default="./workspace",
        description="Allowed directories for filesystem MCP server"
    )

    mcp_fetch_command: str = Field(
        default="python",
        description="Command used to start the fetch MCP server"
    )
    mcp_fetch_args: str = Field(
        default="-m,mcp_server_fetch",
        description="Comma-separated args for fetch MCP server"
    )

    mcp_filesystem_command: str = Field(
        default="npx",
        description="Command used to start the filesystem MCP server"
    )
    mcp_filesystem_args: str = Field(
        default="-y,@modelcontextprotocol/server-filesystem,./workspace",
        description="Comma-separated args for filesystem MCP server"
    )

    # ==============================
    # AGENT SAFETY
    # ==============================

    max_steps: int = Field(
        default=10,
        description="Maximum number of agent planning steps"
    )
    max_retries: int = Field(
        default=2,
        description="Maximum retries per tool call"
    )

    # ==============================
    # SETTINGS CONFIG
    # ==============================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        case_sensitive=False
    )

    # ==============================
    # VALIDATORS
    # ==============================

    @field_validator("llm_backend")
    @classmethod
    def validate_llm_backend(cls, value: str) -> str:
        value = value.lower()
        if value not in {"groq", "ollama"}:
            raise ValueError("llm_backend must be either 'groq' or 'ollama'")
        return value

    @field_validator("groq_api_key")
    @classmethod
    def validate_groq_key(cls, value: str | None, info):
        if info.data.get("llm_backend") == "groq" and not value:
            raise ValueError("GROQ_API_KEY must be set when using Groq backend")
        return value

    # ==============================
    # HELPERS
    # ==============================

    @property
    def is_groq(self) -> bool:
        return self.llm_backend == "groq"

    @property
    def is_ollama(self) -> bool:
        return self.llm_backend == "ollama"

    @property
    def active_llm_base_url(self) -> str:
        return self.groq_base_url if self.is_groq else self.ollama_base_url

    @property
    def active_llm_model(self) -> str:
        return self.groq_model if self.is_groq else self.ollama_model

    @property
    def fetch_args_list(self) -> list[str]:
        return [arg.strip() for arg in self.mcp_fetch_args.split(",")]

    @property
    def filesystem_args_list(self) -> list[str]:
        return [arg.strip() for arg in self.mcp_filesystem_args.split(",")]


# Singleton-style access
settings = Settings()
