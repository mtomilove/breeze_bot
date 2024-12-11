from typing import Final

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from breeze_bot.app.commands import CreateManagerCommand
from breeze_bot.app.deps import Container
from breeze_bot.handlers.entities import ManagerId, ManagerModel
from breeze_bot.handlers.managers import IManagersHandler

TAG: Final[str] = "managers"
PREFIX: Final[str] = f"/{TAG}"
router: Final[APIRouter] = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/get_manager/{manager_id}")
@inject
async def get_manager(
        manager_id: ManagerId,
        managers_handler: IManagersHandler = Depends(Provide[Container.managers_handler])
) -> ManagerModel:
    return await managers_handler.get_manager(manager_id)


@router.get("/get_all_managers")
@inject
async def get_all_managers(
        managers_handler: IManagersHandler = Depends(Provide[Container.managers_handler])
) -> list[ManagerModel]:
    return await managers_handler.get_all_managers()


@router.post("/create_manager")
@inject
async def create_manager(
        command: CreateManagerCommand,
        managers_handler: IManagersHandler = Depends(Provide[Container.managers_handler])
) -> None:
    await managers_handler.create_manager(command)


@router.patch("/change_manager")
@inject
async def change_manager(
        model: ManagerModel,
        managers_handler: IManagersHandler = Depends(Provide[Container.managers_handler])
) -> None:
    await managers_handler.change_manager(model)


@router.delete("/delete_manager")
@inject
async def delete_manager(
        manager_id: ManagerId,
        managers_handler: IManagersHandler = Depends(Provide[Container.managers_handler])
) -> None:
    await managers_handler.delete_manager(manager_id)
