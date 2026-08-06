from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./markosdev.db"
    cors_origins: str = "*"
    admin_password: str = ""
    debug: bool = False
    openrouter_api_key: str = ""
    openrouter_model: str = ""
    n8n_webhook_url: str = ""
    enable_docs: bool = False

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()