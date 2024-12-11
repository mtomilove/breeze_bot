from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.orm import Mapped


class Identifiable:
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)


class Timestampable:
    created_at: Mapped[datetime] = Column(DateTime, default=func.now())
    deleted_at: Mapped[datetime] = Column(DateTime, nullable=True)
