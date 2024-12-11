import abc
from contextlib import AbstractAsyncContextManager
from typing import Callable, Sequence

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from breeze_bot.app.commands import CreateBidCategoryCommand
from breeze_bot.infra.database.models import BidCategoryORM
from breeze_bot.handlers.entities import BidCategoryId, BidCategoryModel
from breeze_bot.repository.errors import NotFoundError


class IBidCategoriesRepository(abc.ABC):

    @abc.abstractmethod
    async def get_by_id(self, bid_category_id: BidCategoryId) -> BidCategoryORM:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(self) -> Sequence[BidCategoryORM]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create(self, command: CreateBidCategoryCommand) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def update(self, model: BidCategoryModel) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, bid_category_id: BidCategoryId) -> None:
        raise NotImplementedError


class BidCategoriesRepository(IBidCategoriesRepository):

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self._session_factory = session_factory

    async def get_by_id(self, bid_category_id: BidCategoryId) -> BidCategoryORM:
        async with self._session_factory() as session:
            result = await session.execute(select(BidCategoryORM).where(BidCategoryORM.id == bid_category_id))
            if bid_category_row := result.scalar_one_or_none():
                return bid_category_row
            raise NotFoundError

    async def get_all(self) -> Sequence[BidCategoryORM]:
        async with self._session_factory() as session:
            result = await session.execute(select(BidCategoryORM))
            if bid_categories_row := result.scalars().all():
                return bid_categories_row
            raise NotFoundError

    async def create(self, command: CreateBidCategoryCommand) -> None:
        async with self._session_factory() as session:
            session.add(BidCategoryORM(**command.model_dump()))
            await session.commit()

    async def update(self, model: BidCategoryModel) -> None:
        async with self._session_factory() as session:
            query = update(BidCategoryORM).where(BidCategoryORM.id == model.id).values(**model.model_dump())
            await session.execute(query)
            await session.commit()

    async def delete(self, bid_category_id: BidCategoryId) -> None:
        async with self._session_factory() as session:
            query = delete(BidCategoryORM).where(BidCategoryORM.id == bid_category_id)
            await session.execute(query)
            await session.commit()
