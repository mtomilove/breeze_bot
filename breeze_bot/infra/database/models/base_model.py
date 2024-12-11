from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


class BaseORMModel(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData()
