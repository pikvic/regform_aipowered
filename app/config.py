from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    yandex_client_id: str
    yandex_client_secret: str
    secret_key: str
    database_url: str
    
    class Config:
        env_file = ".env"

settings = Settings()