import abc

from breeze_bot.app.commands import CreateBidCommand
from breeze_bot.handlers.entities import BidId, BidModel
from breeze_bot.repository.bids import IBidsRepository


class IBidsHandler(abc.ABC):

    @abc.abstractmethod
    async def get_all_bids(self) -> list[BidModel]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_bid(self, command: CreateBidCommand) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_bid(self, bid_id: BidId) -> None:
        raise NotImplementedError


class BidsHandler(IBidsHandler):

    def __init__(self, bids_repository: IBidsRepository) -> None:
        self._bids_repository = bids_repository

    async def get_all_bids(self) -> list[BidModel]:
        bids = await self._bids_repository.get_all()
        return [BidModel.model_validate(bid) for bid in bids]

    async def create_bid(self, command: CreateBidCommand) -> None:
        await self._bids_repository.create(command)

    async def delete_bid(self, bid_id: BidId) -> None:
        await self._bids_repository.delete(bid_id)
