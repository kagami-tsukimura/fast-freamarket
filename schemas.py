from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ItemStatus(Enum):
    ON_SALE = "ON_SALE"
    SOLD_OUT = "SOLD_OUT"


class ItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=20, examples=["PC"])
    price: int = Field(gt=0, examples=[50000])
    description: Optional[str] = Field(None, examples=["新品です"])


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=20, examples=["PC"])
    price: Optional[int] = Field(None, gt=0, examples=[50000])
    description: Optional[str] = Field(None, examples=["新品です"])
    status: Optional[ItemStatus] = Field(None, examples=[ItemStatus.SOLD_OUT])
