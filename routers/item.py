from typing import List, Optional

from fastapi import APIRouter

from cruds import item as item_cruds
from schemas import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.get("", response_model=List[ItemResponse])
async def find_all():
    """
    全てのアイテムを取得します。
    """

    return item_cruds.find_all()


@router.get("/{id}", response_model=Optional[ItemResponse])
async def find_by_id(id: int):
    """
    指定したIDのアイテムを取得します。
    """

    return item_cruds.find_by_id(id)


@router.get("/")
async def find_by_name(name: str, response_model=List[ItemResponse]):
    """
    指定した名前のアイテムを先頭一致で取得します。
    """

    return item_cruds.find_by_name(name)


@router.post("", response_model=ItemResponse)
async def create(create_item: ItemCreate):
    """
    アイテムを新規登録します。
    """

    return item_cruds.create(create_item)


@router.put("/{id}", response_model=Optional[ItemResponse])
async def update(id: int, update_item: ItemUpdate):
    """
    指定したIDのアイテムを更新します。
    """

    return item_cruds.update(id, update_item)


@router.delete("/{id}", response_model=Optional[ItemResponse])
async def delete(id: int):
    """
    指定したIDのアイテムを削除します。
    """

    return item_cruds.delete(id)
