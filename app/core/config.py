from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int

    ENDPOINT: str
    CHAT_PATH: str

    class Config:
        env_file = ".env"

# 全局配置实例
settings = Settings()