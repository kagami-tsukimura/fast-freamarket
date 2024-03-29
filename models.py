from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp

from database import Base
from schemas import ItemStatus


class Item(Base):
    __tablename__ = "items"

    id = Column(
        Integer,
        primary_key=True,
    )
    name = Column(String, unique=True, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(String, nullable=True)
    status = Column(Enum(ItemStatus), nullable=False, default=ItemStatus.ON_SALE)
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime,
        default=current_timestamp(),
        onupdate=current_timestamp(),
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", back_populates="items")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    salt = Column(String, nullable=False)
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime,
        default=current_timestamp(),
        onupdate=current_timestamp(),
    )

    items = relationship("Item", back_populates="user")


# ForeignKeyのテスト
class ItemSub(Base):
    __tablename__ = "items_sub"

    id = Column(
        Integer,
        primary_key=True,
    )
    name = Column(String, ForeignKey("items.name"), unique=True, nullable=False)
    created_at = Column(DateTime, default=current_timestamp())
    updated_at = Column(
        DateTime,
        default=current_timestamp(),
        onupdate=current_timestamp(),
    )
