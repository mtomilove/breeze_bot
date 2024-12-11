import abc
from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence

from sqlalchemy import delete, update, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from breeze_bot.app.commands import CreateEmployeeCommand
from breeze_bot.infra.database.models.models import  EmployeeORM
from breeze_bot.handlers.entities import EmployeeId, EmployeeModel
from breeze_bot.repository.errors import NotFoundError


class IEmployeesRepository(abc.ABC):

    @abc.abstractmethod
    async def get_by_id(self, employee_id: EmployeeId) -> EmployeeORM:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(self) -> Sequence[EmployeeORM]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, command: CreateEmployeeCommand) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, model: EmployeeModel) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, employee_id: EmployeeId) -> None:
        raise NotImplementedError


class EmployeesRepository(IEmployeesRepository):

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def get_by_id(self, employee_id: EmployeeId) -> EmployeeORM:
        async with self._session_factory() as session:
            result = await session.execute(select(EmployeeORM).where(EmployeeORM.id == employee_id))
            if employee_row := result.scalar_one_or_none():
                return employee_row
            raise NotFoundError

    async def get_all(self) -> Sequence[EmployeeORM]:
        async with self._session_factory() as session:
            result = await session.execute(select(EmployeeORM).options(subqueryload(EmployeeORM.bids)))
            if employee_rows := result.scalars().all():
                return employee_rows
            raise NotFoundError

    async def create(self, command: CreateEmployeeCommand) -> None:
        async with self._session_factory() as session:
            session.add(EmployeeORM(**command.model_dump()))
            await session.commit()

    async def update(self, model: EmployeeModel) -> None:
        async with self._session_factory() as session:
            query = update(EmployeeORM).where(EmployeeORM.id == model.id).values(**model.model_dump())
            await session.execute(query)
            await session.commit()

    async def delete(self, employee_id: EmployeeId) -> None:
        async with self._session_factory() as session:
            query = delete(EmployeeORM).where(EmployeeORM.id == employee_id)
            await session.execute(query)
            await session.commit()
