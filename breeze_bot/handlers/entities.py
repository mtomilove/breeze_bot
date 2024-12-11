import datetime
from typing import NewType

from pydantic import BaseModel

BidId = NewType("BidId", int)
EmployeeId = NewType("EmployeeId", int)
ManagerId = NewType("ManagerId", int)
PositionId = NewType("PositionId", int)
BidCategoryId = NewType("BidCategoryId", int)

Nickname = NewType("Nickname", str)


class BaseBotModel(BaseModel):

    class Config:
        from_attributes = True


class EmployeeModel(BaseBotModel):
    id: EmployeeId
    name: str
    surname: str
    nickname: str
    position_id: PositionId


class BidModel(BaseBotModel):
    id: BidId
    address: str
    start_dttm: datetime.datetime
    planned_end_dttm: datetime.datetime
    actual_end_dttm: datetime.datetime
    material_delivery_dttm: datetime.datetime
    employees: list[EmployeeModel]


class ManagerModel(BaseBotModel):
    id: EmployeeId
    name: str
    surname: str
    nickname: str


class BidCategoryModel(BaseBotModel):
    id: BidCategoryId
    name: str
