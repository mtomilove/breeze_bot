import abc

from breeze_bot.app.commands import CreateManagerCommand
from breeze_bot.handlers.entities import ManagerId, ManagerModel
from breeze_bot.repository.managers import IManagersRepository


class IManagersHandler(abc.ABC):

    @abc.abstractmethod
    async def get_manager(self, manager_id: ManagerId) -> ManagerModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_managers(self) -> list[ManagerModel]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_manager(self, command: CreateManagerCommand) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def change_manager(self, model: ManagerModel) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_manager(self, manager_id: ManagerId) -> None:
        raise NotImplementedError


class ManagersHandler(IManagersHandler):

    def __init__(self, managers_repository: IManagersRepository) -> None:
        self._managers_repository = managers_repository

    async def get_manager(self, manager_id: ManagerId) -> ManagerModel:
        manager = await self._managers_repository.get_by_id(manager_id)
        return ManagerModel.model_validate(manager)

    async def get_all_managers(self) -> list[ManagerModel]:
        managers = await self._managers_repository.get_all()
        return [ManagerModel.model_validate(manager) for manager in managers]

    async def create_manager(self, command: CreateManagerCommand) -> None:
        await self._managers_repository.create(command)

    async def change_manager(self, model: ManagerModel) -> None:
        await self._managers_repository.update(model)

    async def delete_manager(self, manager_id: ManagerId) -> None:
        await self._managers_repository.delete(manager_id)
