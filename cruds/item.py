from enum import Enum
from typing import List, Optional

from fastapi import HTTPException


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
    Item(
        id=3,
        name="Book",
        price=3000,
        description="Python",
        status=ItemStatus.ON_SALE,
    ),
]


def find_all() -> List[Item]:
    """
    全てのアイテムを取得します。
    """

    return items


def find_by_id(item_id: int) -> Item:
    """
    指定したIDのアイテムを取得します。

    Args:
        item_id (int): アイテムID

    Returns:
        Item: 指定したIDのアイテム
    """

    # NOTE: 複数の候補が存在する場合、最初の候補を返す
    # NOTE: 該当する候補がない場合、Noneを返す
    return next((item for item in items if item.id == item_id), None)


def find_by_name(name: str) -> Item:
    """
    指定した名前のアイテムを部分一致で取得します。

    Args:
        name (str): アイテム名

    Returns:
        Item: 指定した名前のアイテム
    """

    filtered_items = [item for item in items if name in item.name]

    return filtered_items if filtered_items else None


def create(create_item) -> Item:
    """
    アイテムを新規登録します。

    Args:
        create_item (Item): 登録するアイテム

    Returns:
        Item: 登録したアイテム
    """
    new_item = Item(
        len(items) + 1,
        create_item.get("name"),
        create_item.get("price"),
        create_item.get("description"),
        ItemStatus.ON_SALE,
    )
    items.append(new_item)

    return new_item


def update(id: int, update_item) -> Item:
    """
    アイテムを更新します。

    Args:
        id (int): アイテムID
        update_item (Item): 更新するアイテム

    Returns:
        Item: 更新したアイテム
    """
    item = find_by_id(id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.name = update_item.get("name", item.name)
    item.price = update_item.get("price", item.price)
    item.description = update_item.get("description", item.description)
    item.status = update_item.get("status", item.status)
    return item
