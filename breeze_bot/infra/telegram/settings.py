from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    token: str

    model_config = SettingsConfigDict(env_prefix='BOT_')