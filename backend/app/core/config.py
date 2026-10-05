from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Aegis"
    DATABASE_URL: str = "sqlite:///./aegis.db"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3"
    API_PREFIX: str = "/api/v1"

    # -----------------------------------------------------------------------
    # JWT / Authentication
    # -----------------------------------------------------------------------
    # WARNING: The default below is a DEV-ONLY placeholder.
    # In any non-local environment you MUST override JWT_SECRET_KEY via .env
    # or an environment variable.  Never commit a real secret to source control.
    # Generate a secure key: python -c "import secrets; print(secrets.token_hex(32))"
    JWT_SECRET_KEY: str = "DEV_ONLY_CHANGE_ME_09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

