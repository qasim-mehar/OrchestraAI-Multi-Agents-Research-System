from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MISTRAL_API_KEY: str
    TAVILY_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
