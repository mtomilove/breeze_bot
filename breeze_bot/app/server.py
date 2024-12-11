from pydantic_settings import BaseSettings, SettingsConfigDict
from uvicorn import Server, Config


class ServerSettings(BaseSettings):
    app: str = 'breeze_bot.app.app:app'
    workers: int = 2
    host: str = '0.0.0.0'
    port: int = 8000
    timeout_keep_alive: int = 30

    model_config = SettingsConfigDict(env_prefix='SERVER_')

settings = ServerSettings()
uvicorn_server = Server(Config(**settings.model_dump()))
