from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class PGSettings(BaseSettings):
    host: str
    port: int
    username: str
    password: str
    name: str
    echo: bool
    pool_size: int
    max_overflow: int

    model_config = SettingsConfigDict(env_prefix='PG_')

    @cached_property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


settings = PGSettings()
