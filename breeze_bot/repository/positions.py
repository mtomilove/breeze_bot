import abc
from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from breeze_bot.app.commands import CreatePositionCommand
from breeze_bot.infra.database.models import PositionORM
from breeze_bot.handlers.entities import PositionId


class IPositionsRepository(abc.ABC):

    @abc.abstractmethod
    async def create(self, command: CreatePositionCommand) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, position_id: PositionId):
        raise NotImplementedError


class PositionsRepository(IPositionsRepository):

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def create(self, command: CreatePositionCommand) -> None:
        async with self._session_factory() as session:
            session.add(PositionORM(**command.model_dump()))
            await session.commit()

    async def delete(self, position_id: PositionId) -> None:
        async with self._session_factory() as session:
            query = delete(PositionORM).where(PositionORM.id == position_id)
            await session.execute(query)
            await session.commit()
