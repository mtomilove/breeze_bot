from datetime import datetime
from typing import Sequence

from pydantic import BaseModel

from breeze_bot.handlers.entities import Nickname, PositionId, BidCategoryId, EmployeeId


class BaseCommand(BaseModel):
    ...


class CreateEmployeeCommand(BaseCommand):
    name: str
    surname: str
    nickname: Nickname
    position_id: PositionId


class CreateManagerCommand(BaseCommand):
    name: str
    surname: str
    nickname: Nickname


class CreateBidCategoryCommand(BaseCommand):
    name: str


class CreateBidCommand(BaseCommand):
    address: str
    start_dttm: datetime = datetime.now()
    planned_end_dttm: datetime
    category_id: BidCategoryId
    employees_id: Sequence[EmployeeId]


class CreatePositionCommand(BaseCommand):
    name: str
