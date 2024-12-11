from typing import Final

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from breeze_bot.app.deps import Container
from breeze_bot.app.commands import CreatePositionCommand
from breeze_bot.handlers.entities import PositionId
from breeze_bot.handlers.positions import IPositionsHandler

TAG: Final[str] = "positions"
PREFIX: Final[str] = f"/{TAG}"
router: Final[APIRouter] = APIRouter(prefix=PREFIX, tags=[TAG])


@router.post("/create_position")
@inject
async def create_position(
        command: CreatePositionCommand,
        positions_handler: IPositionsHandler = Depends(Provide[Container.positions_handler])
) -> None:
    await positions_handler.create_position(command)


@router.delete("/delete_position")
@inject
async def delete_position(
        position_id: PositionId,
        positions_handler: IPositionsHandler = Depends(Provide[Container.positions_handler])
) -> None:
    await positions_handler.delete_position(position_id)
