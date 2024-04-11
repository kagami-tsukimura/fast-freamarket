from typing import List

from sqlalchemy.orm import Session

from models import Item
from schemas import ItemCreate, ItemUpdate


def find_all(db: Session) -> List[Item]:
    """
    全てのアイテムを取得します。

    Args:
        db (Session): データベースセッション

    Returns:
        List[Item]: 取得した全アイテムのリスト
    """

    return db.query(Item).order_by(Item.id).all()


def find_by_id(db: Session, item_id: int, user_id: int) -> Item:
    """
    指定したIDのアイテムを取得します。

    Args:
        db (Session): データベースセッション
        item_id (int): アイテムID

    Returns:
        Item: 指定したIDのアイテム
    """

    # NOTE: 複数の候補が存在する場合は最初の候補を返す
    return (
        db.query(Item)
        .filter(Item.id == item_id)
        .filter(Item.user_id == user_id)
        .first()
    )


def find_by_id_nonfil(db: Session, item_id: int) -> Item:
    """
    指定したIDのアイテムを取得します。

    Args:
        db (Session): データベースセッション
        item_id (int): アイテムID

    Returns:
        Item: 指定したIDのアイテム
    """

    # NOTE: 複数の候補が存在する場合は最初の候補を返す
    return db.query(Item).filter(Item.id == item_id).first()


def find_by_name(db: Session, name: str) -> List[Item]:
    """
    指定した名前のアイテムを部分一致で取得します。

    Args:
        db (Session): データベースセッション
        name (str): アイテム名

    Returns:
        Item: 指定した名前のアイテム
    """

    return db.query(Item).filter(Item.name.contains(name)).order_by(Item.id).all()


def create(db: Session, create_item: ItemCreate, user_id: int) -> Item:
    """
    アイテムを新規登録します。

    Args:
        db (Session): データベースセッション
        create_item (ItemCreate): 登録するアイテム

    Returns:
        Item: 登録したアイテム
    """

    new_item = Item(**create_item.model_dump(), user_id=user_id)
    db.add(new_item)
    db.commit()

    return new_item


def message_multiple(db: Session, req_ids: List[int]) -> List[dict]:
    """
    複数アイテムを疎通します。

    Args:
        db (Session): データベースセッション
        message_item (ItemMessageCreate): 疎通するアイテムのデータ

    Returns:
        Item: 疎通したアイテム
    """

    res_ids = []
    for id in req_ids:
        item = find_by_id_nonfil(db, id)
        if not item:
            return None
        res_ids.append({"res": "ok", "id": item.id, "name": item.name})

    return res_ids


def update(db: Session, id: int, update_item: ItemUpdate, user_id: int) -> Item:
    """
    指定したIDのアイテムを更新します。

    Args:
        db (Session): データベースセッション
        id (int): アイテムID
        update_item (ItemUpdate): 更新するアイテム

    Returns:
        Item: 更新したアイテム
    """

    item = find_by_id(db, id, user_id)
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


def delete(db: Session, id: int, user_id: int):
    """
    指定したIDのアイテムを削除します。

    Args:
        db (Session): データベースセッション
        id (int): アイテムID

    Returns:
        Item: 削除したアイテム
    """

    item = find_by_id(db, id, user_id)
    # early return
    if not item:
        return None

    db.delete(item)
    db.commit()

    return item
