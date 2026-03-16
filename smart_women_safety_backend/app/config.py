from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Change this to lowercase to match your error log's request
    database_url: str = "sqlite:///./data/safety_app.db"
    secret_key: str = "your_super_secret_key_here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()