from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime, Enum, Integer, String
from sqlalchemy.sql.functions import current_timestamp

from database import Base
from schemas import ItemStatus


def current_time():
    return datetime.now(ZoneInfo("Asia/Tokyo"))


class Item(Base):
    __tablename__ = "items"

    id = Column(
        Integer,
        primary_key=True,
    )
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(ItemStatus), nullable=False, default=ItemStatus.ON_SALE)
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime,
        default=current_timestamp(),
        onupdate=current_timestamp(),
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime,
        default=current_timestamp(),
        onupdate=current_timestamp(),
    )
