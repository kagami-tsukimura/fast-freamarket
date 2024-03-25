from fastapi import APIRouter, Body

from cruds import item as item_cruds

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.get("")
async def find_all():
    """
    全てのアイテムを取得します。
    """

    return item_cruds.find_all()


@router.get("/{id}")
async def find_by_id(id: int):
    """
    指定したIDのアイテムを取得します。
    """

    return item_cruds.find_by_id(id)


@router.get("/")
async def find_by_name(name: str):
    """
    指定した名前のアイテムを先頭一致で取得します。
    """

    return item_cruds.find_by_name(name)


@router.post("")
async def create(create_item=Body(...)):
    """
    アイテムを新規登録します。
    """

    return item_cruds.create(create_item)


@router.put("/{id}")
async def update(id: int, update_item=Body(...)):
    """
    指定したIDのアイテムを更新します。
    """

    return item_cruds.update(id, update_item)


@router.delete("/{id}")
async def delete(id: int):
    """
    指定したIDのアイテムを削除します。
    """

    return item_cruds.delete(id)
