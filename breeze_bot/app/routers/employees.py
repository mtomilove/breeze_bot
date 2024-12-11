from typing import Final

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from breeze_bot.app.deps import Container
from breeze_bot.app.commands import CreateEmployeeCommand
from breeze_bot.handlers.employees import IEmployeesHandler
from breeze_bot.handlers.entities import EmployeeId, EmployeeModel

TAG: Final[str] = "employees"
PREFIX: Final[str] = f"/{TAG}"
router: Final[APIRouter] = APIRouter(prefix=PREFIX, tags=[TAG])


@router.get("/get_employee/{employee_id}")
@inject
async def get_employee(
        employee_id: EmployeeId,
        employees_handler: IEmployeesHandler = Depends(Provide[Container.employees_handler])
) -> EmployeeModel:
    return await employees_handler.get_employee(employee_id)


@router.get("/get_all_employees")
@inject
async def get_all_employees(
        employees_handler: IEmployeesHandler = Depends(Provide[Container.employees_handler])
) -> list[EmployeeModel]:
    return await employees_handler.get_all_employees()


@router.post("/create_employee")
@inject
async def create_employee(
        command: CreateEmployeeCommand,
        employees_handler: IEmployeesHandler = Depends(Provide[Container.employees_handler])
) -> None:
    await employees_handler.create_employee(command)


@router.patch("/change_employee")
@inject
async def change_employee(
        model: EmployeeModel,
        employees_handler: IEmployeesHandler = Depends(Provide[Container.employees_handler])
) -> None:
    await employees_handler.change_employee(model)


@router.delete("/delete_employee")
@inject
async def delete_employee(
        employee_id: EmployeeId,
        employees_handler: IEmployeesHandler = Depends(Provide[Container.employees_handler])
) -> None:
    await employees_handler.delete_employee(employee_id)
