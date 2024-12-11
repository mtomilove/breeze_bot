import abc

from breeze_bot.app.commands import CreateEmployeeCommand
from breeze_bot.handlers.entities import EmployeeId, EmployeeModel
from breeze_bot.repository.employees import IEmployeesRepository


class IEmployeesHandler(abc.ABC):

    @abc.abstractmethod
    async def get_employee(self, employee_id: EmployeeId) -> EmployeeModel:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_employees(self) -> list[EmployeeModel]:
        raise NotImplementedError

    @abc.abstractmethod
    async def create_employee(self, command: CreateEmployeeCommand) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def change_employee(self, model: EmployeeModel) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_employee(self, employee_id: EmployeeId) -> None:
        raise NotImplementedError


class EmployeesHandler(IEmployeesHandler):

    def __init__(self, employees_repository: IEmployeesRepository) -> None:
        self._employees_repository = employees_repository

    async def get_employee(self, employee_id: EmployeeId) -> EmployeeModel:
        employee = await self._employees_repository.get_by_id(employee_id)
        return EmployeeModel.model_validate(employee)

    async def get_all_employees(self) -> list[EmployeeModel]:
        employees = await self._employees_repository.get_all()
        return [EmployeeModel.model_validate(employee) for employee in employees]

    async def create_employee(self, command: CreateEmployeeCommand) -> None:
        await self._employees_repository.create(command)

    async def change_employee(self, model: EmployeeModel) -> None:
        await self._employees_repository.update(model)

    async def delete_employee(self, employee_id: EmployeeId) -> None:
        await self._employees_repository.delete(employee_id)
