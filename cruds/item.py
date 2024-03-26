from typing import List

from sqlalchemy.orm import Session

from models import Item
from schemas import ItemCreate, ItemUpdate

# def find_all() -> List[Item]:
#     """
#     全てのアイテムを取得します。
#     """

#     return items


# def find_by_id(item_id: int) -> Item:
#     """
#     指定したIDのアイテムを取得します。

#     Args:
#         item_id (int): アイテムID

#     Returns:
#         Item: 指定したIDのアイテム
#     """

#     # NOTE: 複数の候補が存在する場合、最初の候補を返す
#     # NOTE: 該当する候補がない場合、Noneを返す
#     return next((item for item in items if item.id == item_id), None)


# def find_by_name(name: str) -> Item:
#     """
#     指定した名前のアイテムを先頭一致で取得します。

#     Args:
#         name (str): アイテム名

#     Returns:
#         Item: 指定した名前のアイテム
#     """

#     filtered_items = [item for item in items if item.name.startswith(name)]

#     return filtered_items if filtered_items else None


def create(db: Session, create_item: ItemCreate) -> Item:
    """
    アイテムをDBに新規登録します.

    Args:
        create_item (ItemCreate): 登録するアイテム

    Returns:
        Item: 登録したアイテム
    """

    new_item = Item(**create_item.model_dump())
    db.add(new_item)
    db.commit()

    return new_item


# def update(id: int, update_item: ItemUpdate) -> Item:
#     """
#     アイテムを更新します。

#     Args:
#         id (int): アイテムID
#         update_item (ItemUpdate): 更新するアイテム

#     Returns:
#         Item: 更新したアイテム
#     """

#     item = find_by_id(id)
#     # early return
#     if not item:
#         return None

#     item.name = update_item.name if update_item.name else item.name
#     item.price = update_item.price if update_item.price else item.price
#     item.description = (
#         update_item.description if update_item.description else item.description
#     )
#     item.status = update_item.status if update_item.status else item.status

#     return item


# def delete(id: int):
#     """
#     アイテムを削除します。

#     Args:
#         id (int): アイテムID
#         update_item (Item): 更新するアイテム

#     Returns:
#         Item: 削除したアイテム
#     """

#     item = find_by_id(id)
#     # early return
#     if not item:
#         return None

#     items.remove(item)

#     return item
