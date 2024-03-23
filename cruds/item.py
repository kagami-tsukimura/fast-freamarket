from enum import Enum
from typing import List, Optional


class ItemStatus(Enum):
    ON_SALE = "ON_SALE"
    SOLD_OUT = "SOLD_OUT"


class Item:
    def __init__(
        self,
        id: int,
        name: str,
        price: int,
        description: Optional[str],
        status: ItemStatus,
    ):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
        self.status = status


items = [
    Item(
        id=1,
        name="PC",
        price=100000,
        description="Windows11",
        status=ItemStatus.ON_SALE,
    ),
    Item(
        id=2,
        name="iPhone",
        price=120000,
        description="iPhone15",
        status=ItemStatus.ON_SALE,
    ),
    Item(
        id=3,
        name="Book",
        price=4000,
        description="FastAPI",
        status=ItemStatus.SOLD_OUT,
    ),
]


def find_all() -> List[Item]:
    return items
