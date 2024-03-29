from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import Item, ItemSub
from schemas import ItemSubCreate, ItemSubUpdate


def find_all(db: Session) -> List[ItemSub]:
    """
    全てのItemSubを取得します。

    Args:
        db (Session): データベースセッション

    Returns:
        List[ItemSub]: 取得した全ItemSubのリスト
    """

    return db.query(ItemSub).order_by(ItemSub.id).all()


def find_by_id(db: Session, item_sub_id: int) -> ItemSub:
    """
    指定したIDのItemSubを取得します。

    Args:
        db (Session): データベースセッション
        item_sub_id (int): ItemSubのID

    Returns:
        ItemSub: 指定したIDのItemSub
    """

    # NOTE: 複数の候補が存在する場合は最初の候補を返す
    return db.query(ItemSub).filter(ItemSub.id == item_sub_id).first()


def create(db: Session, create_item: ItemSubCreate) -> ItemSub:
    """
    ItemSubを新規登録します。

    Args:
        db (Session): データベースセッション
        create_item (ItemSubCreate): 登録するItemSub

    Returns:
        ItemSub: 登録したItemSub
    """

    new_item_sub = ItemSub(**create_item.model_dump())
    db.add(new_item_sub)
    db.commit()

    return new_item_sub


def update(db: Session, id: int, update_item: ItemSubUpdate) -> ItemSub:
    """
    指定したIDのItemSubを更新します。

    Args:
        db (Session): データベースセッション
        id (int): ItemSubのID
        update_item (ItemSubUpdate): 更新するItemSub

    Returns:
        ItemSub: 更新したItemSub
    """

    item_sub = find_by_id(db, id)

    # early return
    if not item_sub:
        raise HTTPException(status_code=404, detail="ItemSub not found")

    # item_sub.nameがitemテーブルに存在するか確認
    item = db.query(Item).filter(Item.name == update_item.name).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item name not found")

    # # early return
    # if not item_sub:
    #     return None

    item_sub.name = update_item.name if update_item.name else item_sub.name

    db.add(item_sub)
    db.commit()

    return item_sub


def delete(db: Session, id: int):
    """
    指定したIDのItemSubを削除します。

    Args:
        db (Session): データベースセッション
        id (int): ItemSubのID

    Returns:
        ItemSub: 削除したItemSub
    """

    item_sub = find_by_id(db, id)
    # early return
    if not item_sub:
        return None

    db.delete(item_sub)
    db.commit()

    return item_sub
