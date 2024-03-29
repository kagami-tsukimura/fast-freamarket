from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from starlette import status

from cruds import item_sub as item_sub_cruds
from database import get_db
from schemas import ItemSubCreate, ItemSubResponse, ItemSubUpdate

DbDependency = Annotated[Session, Depends(get_db)]

router = APIRouter(
    prefix="/item_subs",
    tags=["item_subs"],
)


# 以下にルーティングを追加
# 例: item_subの全てのアイテムを取得する
@router.get("", response_model=List[ItemSubResponse], status_code=status.HTTP_200_OK)
async def find_all(db: DbDependency):
    return item_sub_cruds.find_all(db)


# 例: item_subの特定のアイテムを取得する
@router.get("/{id}", response_model=ItemSubResponse, status_code=status.HTTP_200_OK)
async def find_by_id(db: DbDependency, id: int = Path(gt=0)):
    found_item = item_sub_cruds.find_by_id(db, id)
    if not found_item:
        raise HTTPException(status_code=404, detail="ItemSub not found")
    return found_item


# 例: item_subを新規作成する
@router.post("", response_model=ItemSubResponse, status_code=status.HTTP_201_CREATED)
async def create(db: DbDependency, create_item: ItemSubCreate):
    return item_sub_cruds.create(db, create_item)


# 例: item_subを更新する
@router.put("/{id}", response_model=ItemSubResponse, status_code=status.HTTP_200_OK)
async def update(db: DbDependency, update_item: ItemSubUpdate, id: int = Path(gt=0)):
    updated_item = item_sub_cruds.update(db, id, update_item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="ItemSub not updated")
    return updated_item


# 例: item_subを削除する
@router.delete("/{id}", response_model=ItemSubResponse, status_code=status.HTTP_200_OK)
async def delete(db: DbDependency, id: int = Path(gt=0)):
    deleted_item = item_sub_cruds.delete(db, id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="ItemSub not deleted")
    return deleted_item
