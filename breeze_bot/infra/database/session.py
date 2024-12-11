from functools import lru_cache

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker

from breeze_bot.infra.database.settings import settings


@lru_cache(maxsize=1, typed=True)
def async_engine() -> AsyncEngine:
    return create_async_engine(
        url=settings.url,
        echo=settings.echo,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
    )


@lru_cache(maxsize=1, typed=True)
def async_session_factory() -> async_sessionmaker:
    return async_sessionmaker(bind=async_engine())
