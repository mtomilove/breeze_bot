import abc

from breeze_bot.app.commands import CreatePositionCommand
from breeze_bot.handlers.entities import PositionId
from breeze_bot.repository.positions import IPositionsRepository


class IPositionsHandler(abc.ABC):

    @abc.abstractmethod
    async def create_position(self, command: CreatePositionCommand) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_position(self, position_id: PositionId) -> None:
        raise NotImplementedError


class PositionsHandler(IPositionsHandler):

    def __init__(self, positions_repository: IPositionsRepository) -> None:
        self._positions_repository = positions_repository

    async def create_position(self, command: CreatePositionCommand) -> None:
        await self._positions_repository.create(command)

    async def delete_position(self, position_id: PositionId) -> None:
        await self._positions_repository.delete(position_id)
