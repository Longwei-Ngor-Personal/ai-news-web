from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI News Web Digestor API"
    environment: str = "production"
    # SQLite DB stored in ./data/news.db on the host (mapped into container)
    database_url: str = "sqlite:///./data/news.db"

    class Config:
        env_file = ".env"


settings = Settings()
