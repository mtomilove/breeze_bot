from datetime import datetime
from typing import ClassVar

from sqlalchemy import Column, Text, DateTime, String, Integer, ForeignKey, Float
from sqlalchemy.orm import Mapped, relationship

from breeze_bot.infra.database.models.base_model import BaseORMModel
from breeze_bot.infra.database.models.templates import Identifiable, Timestampable


class BidORM(Identifiable, Timestampable, BaseORMModel):
    __tablename__: ClassVar[str] = 'bids'

    address: Mapped[str] = Column(Text, nullable=False)

    start_dttm: Mapped[datetime] = Column(DateTime, nullable=False)
    planned_end_dttm: Mapped[datetime] = Column(DateTime, nullable=False)
    actual_end_dttm: Mapped[datetime] = Column(DateTime, nullable=True)
    material_delivery_dttm: Mapped[datetime] = Column(DateTime, nullable=True)

    category_id: Mapped[int] = Column(Integer, ForeignKey('bid_categories.id'), nullable=False)

    category: Mapped["BidCategoryORM"] = relationship("BidCategoryORM", back_populates="bids")
    spendings: Mapped[list["SpendingORM"]] = relationship("SpendingORM", back_populates="bid")
    comments: Mapped[list["CommentORM"]] = relationship("CommentORM", back_populates="bid")
    employees: Mapped[list["EmployeeORM"]] = relationship(
        'EmployeeORM',
        secondary='bids_x_employees',
        back_populates='bids'
    )


class BidCategoryORM(Identifiable, BaseORMModel):
    __tablename__: ClassVar[str] = 'bid_categories'

    name: Mapped[str] = Column(String(255), nullable=False)

    bids: Mapped[list[BidORM]] = relationship("BidORM", back_populates="category")


class EmployeeORM(Identifiable, Timestampable, BaseORMModel):
    __tablename__: ClassVar[str] = 'employees'

    name: Mapped[str] = Column(Text, nullable=False)
    surname: Mapped[str] = Column(Text, nullable=False)
    nickname: Mapped[str] = Column(Text, nullable=False)

    position_id: Mapped[int] = Column(Integer, ForeignKey('positions.id'), nullable=False)

    position: Mapped["PositionORM"] = relationship("PositionORM", back_populates="employees")
    bids: Mapped[list["BidORM"]] = relationship(
        'BidORM',
        secondary='bids_x_employees',
        back_populates='employees'
    )


class PositionORM(Identifiable, BaseORMModel):
    __tablename__: ClassVar[str] = 'positions'

    name: Mapped[str] = Column(String(255), nullable=False)

    employees: Mapped[list[EmployeeORM]] = relationship("EmployeeORM", back_populates="position")


class XBidEmployee(BaseORMModel):
    __tablename__: ClassVar[str] = 'bids_x_employees'

    bid_id: Mapped[int] = Column(ForeignKey('bids.id'), primary_key=True)
    employee_id: Mapped[int] = Column(ForeignKey('employees.id'), primary_key=True)


class ManagerORM(Identifiable, Timestampable, BaseORMModel):
    __tablename__: ClassVar[str] = 'managers'

    name: Mapped[str] = Column(Text, nullable=False)
    surname: Mapped[str] = Column(Text, nullable=False)
    nickname: Mapped[str] = Column(Text, nullable=False)


class SpendingORM(Identifiable, Timestampable, BaseORMModel):
    __tablename__: ClassVar[str] = 'spendings'

    name: Mapped[str] = Column(Text, nullable=False)
    amount: Mapped[float] = Column(Float, nullable=False)

    bid_id: Mapped[int] = Column(Integer, ForeignKey('bids.id'), nullable=False)

    bid: Mapped["BidORM"] = relationship("BidORM", back_populates="spendings")


class CommentORM(Identifiable, Timestampable, BaseORMModel):
    __tablename__: ClassVar[str] = 'comments'

    comment: Mapped[str] = Column(Text, nullable=False)

    bid_id: Mapped[int] = Column(Integer, ForeignKey('bids.id'), nullable=False)

    bid: Mapped["BidORM"] = relationship("BidORM", back_populates="comments")