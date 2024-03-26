from typing import List

from sqlalchemy.orm import Session

from models import Item
from schemas import ItemCreate, ItemUpdate


def find_all(db: Session) -> List[Item]:
    """
    DBから全てのアイテムを取得します.
    """

    return db.query(Item).order_by(Item.id).all()


def find_by_id(db: Session, item_id: int) -> Item:
    """
    DBから指定したIDのアイテムを取得します.

    Args:
        item_id (int): アイテムID

    Returns:
        Item: 指定したIDのアイテム
    """

    # NOTE: 複数の候補が存在する場合は最初の候補を返す
    return db.query(Item).filter(Item.id == item_id).first()


def find_by_name(db: Session, name: str) -> List[Item]:
    """
    DBから指定した名前のアイテムを部分一致で取得します.

    Args:
        name (str): アイテム名

    Returns:
        Item: 指定した名前のアイテム
    """

    return db.query(Item).filter(Item.name.contains(name)).order_by(Item.id).all()


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


def update(db: Session, id: int, update_item: ItemUpdate) -> Item:
    """
    DBから指定したIDのアイテムを更新します.

    Args:
        id (int): アイテムID
        update_item (ItemUpdate): 更新するアイテム

    Returns:
        Item: 更新したアイテム
    """

    item = find_by_id(db, id)
    # early return
    if not item:
        return None

    item.name = update_item.name if update_item.name else item.name
    item.price = update_item.price if update_item.price else item.price
    item.description = (
        update_item.description if update_item.description else item.description
    )
    item.status = update_item.status if update_item.status else item.status

    db.add(item)
    db.commit()

    return item


def delete(db: Session, id: int):
    """
    DBから指定したIDのアイテムを削除します.

    Args:
        id (int): アイテムID
        update_item (Item): 更新するアイテム

    Returns:
        Item: 削除したアイテム
    """

    item = find_by_id(db, id)
    # early return
    if not item:
        return None

    db.delete(item)
    db.commit()

    return item
