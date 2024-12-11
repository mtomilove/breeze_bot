from typing import Final

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from breeze_bot.app.deps import Container
from breeze_bot.app.commands import CreateBidCategoryCommand
from breeze_bot.handlers.bid_categories import IBidCategoriesHandler
from breeze_bot.handlers.entities import BidCategoryId, BidCategoryModel

TAG: Final[str] = "bid_categories"
PREFIX: Final[str] = f"/{TAG}"
router: Final[APIRouter] = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/get_bid_category/{bid_category_id}")
@inject
async def get_bid_category(
        bid_category_id: BidCategoryId,
        bid_categories_handler: IBidCategoriesHandler = Depends(Provide[Container.bid_categories_handler])
) -> BidCategoryModel:
    return await bid_categories_handler.get_bid_category(bid_category_id)


@router.get("/get_all_bid_categories")
@inject
async def get_all_bid_categories(
        bid_categories_handler: IBidCategoriesHandler = Depends(Provide[Container.bid_categories_handler])
) -> list[BidCategoryModel]:
    return await bid_categories_handler.get_all_bid_categories()


@router.post("/create_bid_category")
@inject
async def create_bid_category(
        command: CreateBidCategoryCommand,
        bid_categories_handler: IBidCategoriesHandler = Depends(Provide[Container.bid_categories_handler])
) -> None:
    await bid_categories_handler.create_bid_category(command)


@router.patch("/change_bid_category")
@inject
async def change_bid_category(
        model: BidCategoryModel,
        bid_categories_handler: IBidCategoriesHandler = Depends(Provide[Container.bid_categories_handler])
) -> None:
    await bid_categories_handler.change_bid_category(model)


@router.delete("/delete_bid_category")
@inject
async def delete_bid_category(
        bid_category_id: BidCategoryId,
        bid_categories_handler: IBidCategoriesHandler = Depends(Provide[Container.bid_categories_handler])
) -> None:
    await bid_categories_handler.delete_bid_category(bid_category_id)
