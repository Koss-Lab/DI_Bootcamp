# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    llm_backend: str = "groq"

    groq_api_key: str | None = None
    groq_base_url: str = "https://api.groq.com/openai/v1"
    groq_model: str = "llama-3.1-70b-versatile"

    ollama_base_url: str = "http://localhost:11434/v1"
    ollama_model: str = "llama3"

    max_steps: int = 4
    max_retries: int = 1

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensitive=False,
    )

    @property
    def active_llm_base_url(self) -> str:
        return self.groq_base_url if self.llm_backend == "groq" else self.ollama_base_url

    @property
    def active_llm_model(self) -> str:
        return self.groq_model if self.llm_backend == "groq" else self.ollama_model


settings = Settings()
