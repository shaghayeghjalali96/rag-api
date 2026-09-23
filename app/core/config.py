from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    ollama_url: str = "http://localhost:11434"
    llm_model: str = "llama3.1:8b"
    embedding_model: str = "nomic-embed-text"
    top_k: int = 5

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
