from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI News Web Digestor API"
    environment: str = "development"
    # For now, simple SQLite for local testing; we can switch to Postgres later.
    database_url: str = "sqlite:///./news.db"

    class Config:
        env_file = ".env"  # will read vars from a .env file in project root


settings = Settings()
