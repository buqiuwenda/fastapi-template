from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int

    class Config:
        env_file = ".env"

# 全局配置实例
settings = Settings()