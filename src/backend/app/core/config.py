from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    secret_key: str
    deepseek_api_key: Optional[str] = None
    signal_service_phone: Optional[str] = None
    signal_cli_path: str = "signal-cli"
    signal_bridge_url: str = "http://host.docker.internal:5005"
    internal_api_key: str = "change_this_internal_key"
    encryption_key: str = ""

    class Config:
        env_file = ".env"

settings = Settings()