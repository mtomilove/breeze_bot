import abc
from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import subqueryload

from breeze_bot.app.commands import CreateBidCommand
from breeze_bot.infra.database.models import XBidEmployee
from breeze_bot.infra.database.models.models import BidORM
from breeze_bot.handlers.entities import BidId
from breeze_bot.repository.errors import NotFoundError


class IBidsRepository(abc.ABC):

    @abc.abstractmethod
    async def get_all(self) -> Sequence[BidORM]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, command: CreateBidCommand) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, bid_id: BidId) -> None:
        raise NotImplementedError


class BidsRepository(IBidsRepository):

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def get_all(self) -> Sequence[BidORM]:
        async with self._session_factory() as session:
            result = await session.execute(select(BidORM).options(subqueryload(BidORM.category)))
            if bid_rows := result.scalars().all():
                return bid_rows
            raise NotFoundError

    async def create(self, command: CreateBidCommand) -> None:
        async with self._session_factory() as session:
            bid_row = BidORM(
                address=command.address,
                start_dttm=command.start_dttm,
                planned_end_dttm=command.planned_end_dttm,
                category_id=command.category_id,
            )
            session.add(bid_row)
            await session.flush()

            session.add_all((XBidEmployee(bid_id=bid_row.id, employee_id=e_id) for e_id in command.employees_id))
            await session.commit()

    async def delete(self, bid_id: BidId) -> None:
        async with self._session_factory() as session:
            await session.execute(delete(XBidEmployee).where(XBidEmployee.bid_id == bid_id))
            await session.execute(delete(BidORM).where(BidORM.id == bid_id))
            await session.commit()
