import abc
from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence

from sqlalchemy import delete, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from breeze_bot.app.commands import CreateManagerCommand
from breeze_bot.infra.database.models.models import  ManagerORM
from breeze_bot.handlers.entities import ManagerId, ManagerModel
from breeze_bot.repository.errors import NotFoundError


class IManagersRepository(abc.ABC):

    @abc.abstractmethod
    async def get_by_id(self, manager_id: ManagerId) -> ManagerModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(self) -> Sequence[ManagerModel]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, command: CreateManagerCommand) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, model: ManagerModel) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, manager_id: ManagerId) -> None:
        raise NotImplementedError


class ManagersRepository(IManagersRepository):

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def get_by_id(self, manager_id: ManagerId) -> ManagerORM:
        async with self._session_factory() as session:
            result = await session.execute(select(ManagerORM).where(ManagerORM.id == manager_id))
            if manager_row := result.scalar_one_or_none():
                return manager_row
            raise NotFoundError

    async def get_all(self) -> Sequence[ManagerORM]:
        async with self._session_factory() as session:
            result = await session.execute(select(ManagerORM))
            if manager_rows := result.scalars().all():
                return manager_rows
            raise NotFoundError

    async def create(self, command: CreateManagerCommand) -> None:
        async with self._session_factory() as session:
            session.add(ManagerORM(**command.model_dump()))
            await session.commit()

    async def delete(self, manager_id: ManagerId) -> None:
        async with self._session_factory() as session:
            query = delete(ManagerORM).where(ManagerORM.id == manager_id)
            await session.execute(query)
            await session.commit()

    async def update(self, model: ManagerModel) -> None:
        async with self._session_factory() as session:
            query = update(ManagerORM).where(ManagerORM.id == model.id).values(**model.model_dump())
            await session.execute(query)
            await session.commit()
