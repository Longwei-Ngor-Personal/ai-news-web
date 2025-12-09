from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI News Web Digestor API"
    environment: str = "development"
    # SQLite DB path inside container. We mapped ./data -> /app/data in docker-compose
    database_url: str = "sqlite:///./data/news.db"

    class Config:
        env_file = ".env"


settings = Settings()
