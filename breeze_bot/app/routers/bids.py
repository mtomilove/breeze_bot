from typing import Final

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from breeze_bot.app.commands import CreateBidCommand
from breeze_bot.app.deps import Container
from breeze_bot.handlers.bids import IBidsHandler
from breeze_bot.handlers.entities import BidId, BidModel

TAG: Final[str] = "bids"
PREFIX: Final[str] = f"/{TAG}"
router: Final[APIRouter] = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/get_all_bids")
@inject
async def get_all_bids(bids_handler: IBidsHandler = Depends(Provide[Container.bids_handler])) -> list[BidModel]:
    return await bids_handler.get_all_bids()


@router.post("/create_bid")
@inject
async def create_bid(
        command: CreateBidCommand,
        bids_handler: IBidsHandler = Depends(Provide[Container.bids_handler]),
) -> None:
    await bids_handler.create_bid(command)


@router.delete("/delete_bid")
@inject
async def delete_bid(
        bid_id: BidId,
        bids_handler: IBidsHandler = Depends(Provide[Container.bids_handler]),
) -> None:
    await bids_handler.delete_bid(bid_id)
