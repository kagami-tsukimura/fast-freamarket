from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from starlette import status

from cruds import item as item_cruds
from database import get_db
from schemas import ItemCreate, ItemResponse, ItemUpdate

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.get("", response_model=List[ItemResponse], status_code=status.HTTP_200_OK)
async def find_all(db: DbDependency):
    """
    全てのアイテムを取得します。
    """

    return item_cruds.find_all(db)


@router.get("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def find_by_id(db: DbDependency, id: int = Path(gt=0)):
    """
    DBから指定したIDのアイテムを取得します.
    """

    found_item = item_cruds.find_by_id(db, id)
    if not found_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return found_item


@router.get("/", response_model=List[ItemResponse], status_code=status.HTTP_200_OK)
async def find_by_name(
    db: DbDependency, name: str = Query(min_length=1, max_length=20)
):
    """
    指定した名前のアイテムを部分一致で取得します.
    """

    found_item = item_cruds.find_by_name(db, name)
    if not found_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return found_item


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create(create_item: ItemCreate, db: DbDependency):
    """
    アイテムを新規登録します.
    """

    return item_cruds.create(db, create_item)


# @router.put("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
# async def update(update_item: ItemUpdate, id: int = Path(gt=0)):
#     """
#     指定したIDのアイテムを更新します。
#     """

#     updated_item = item_cruds.update(id, update_item)
#     if not updated_item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return updated_item


# @router.delete("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
# async def delete(id: int = Path(gt=0)):
#     """
#     指定したIDのアイテムを削除します。
#     """

#     deleted_item = item_cruds.delete(id)
#     if not deleted_item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return deleted_item
