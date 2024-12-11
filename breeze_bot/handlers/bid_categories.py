import abc

from breeze_bot.app.commands import CreateBidCategoryCommand
from breeze_bot.handlers.entities import BidCategoryId, BidCategoryModel
from breeze_bot.repository.bid_categories import IBidCategoriesRepository


class IBidCategoriesHandler(abc.ABC):

    @abc.abstractmethod
    async def get_bid_category(self, bid_category_id: BidCategoryId) -> BidCategoryModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_bid_categories(self) -> list[BidCategoryModel]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_bid_category(self, command: CreateBidCategoryCommand) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def change_bid_category(self, model: BidCategoryModel) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_bid_category(self, bid_category_id: BidCategoryId) -> None:
        raise NotImplementedError


class BidCategoriesHandler(IBidCategoriesHandler):

    def __init__(self, bid_categories_repository: IBidCategoriesRepository) -> None:
        self._bid_categories_repository = bid_categories_repository

    async def get_bid_category(self, bid_category_id: BidCategoryId) -> BidCategoryModel:
        bid_category = await self._bid_categories_repository.get_by_id(bid_category_id)
        return BidCategoryModel.model_validate(bid_category)

    async def get_all_bid_categories(self) -> list[BidCategoryModel]:
        bid_categories = await self._bid_categories_repository.get_all()
        return [BidCategoryModel.model_validate(bid_category) for bid_category in bid_categories]

    async def create_bid_category(self, command: CreateBidCategoryCommand) -> None:
        await self._bid_categories_repository.create(command)

    async def change_bid_category(self, model: BidCategoryModel) -> None:
        await self._bid_categories_repository.update(model)

    async def delete_bid_category(self, bid_category_id: BidCategoryId) -> None:
        await self._bid_categories_repository.delete(bid_category_id)
