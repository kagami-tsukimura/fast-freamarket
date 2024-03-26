from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime, Enum, Integer, String

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
    created_at = Column(DateTime, default=current_time())
    updated_at = Column(
        DateTime,
        default=current_time(),
        onupdate=current_time(),
    )
