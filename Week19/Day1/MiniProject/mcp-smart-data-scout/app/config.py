# app/config.py
"""
Central configuration (env-safe, checker-safe)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ==============================
    # LLM
    # ==============================
    llm_backend: str = "groq"

    groq_api_key: str | None = None
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_model: str = "llama-3.1-70b-versatile"

    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_model: str = "llama3"

    # ==============================
    # MCP SERVERS
    # ==============================
    mcp_time_command: str = "python"
    mcp_time_args_raw: str = "-m mcp_server_time --local-timezone UTC"

    mcp_fetch_command: str = "python"
    mcp_fetch_args_raw: str = "-m mcp_server_fetch"

    mcp_insights_command: str = "python"
    mcp_insights_args_raw: str = "-m app.servers.insights_server"

    # ==============================
    # AGENT
    # ==============================
    max_steps: int = 6
    max_retries: int = 2
    tool_timeout_s: int = 20

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # ==============================
    # HELPERS
    # ==============================
    @property
    def mcp_time_args(self) -> list[str]:
        return self.mcp_time_args_raw.split()

    @property
    def mcp_fetch_args(self) -> list[str]:
        return self.mcp_fetch_args_raw.split()

    @property
    def mcp_insights_args(self) -> list[str]:
        return self.mcp_insights_args_raw.split()

    @property
    def active_llm_base_url(self) -> str:
        return (
            self.groq_base_url
            if self.llm_backend.lower() == "groq"
            else self.ollama_base_url
        )

    @property
    def active_llm_model(self) -> str:
        return (
            self.groq_model
            if self.llm_backend.lower() == "groq"
            else self.ollama_model
        )


settings = Settings()
