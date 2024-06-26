from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, Request
from sqlalchemy.orm import Session
from starlette import status

from cruds import auth as auth_cruds
from cruds import item as item_cruds
from database import get_db
from schemas import (
    DecodedToken,
    ItemCreate,
    ItemMessage,
    ItemMessageResponse,
    ItemResponse,
    ItemUpdate,
)

DbDependency = Annotated[Session, Depends(get_db)]

UserDependency = Annotated[DecodedToken, Depends(auth_cruds.get_current_user)]

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.get("", response_model=List[ItemResponse], status_code=status.HTTP_200_OK)
async def find_all(db: DbDependency):
    """
    全てのアイテムを取得します。

    Args:
        db (DbDependency): データベースセッションの依存関係

    Returns:
        List[ItemResponse]: 取得したアイテムのリスト
    """

    return item_cruds.find_all(db)


@router.get("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def find_by_id(db: DbDependency, user: UserDependency, id: int = Path(gt=0)):
    """
    指定したIDのアイテムを取得します。

    Args:
        db (DbDependency): データベースセッションの依存関係
        id (int): アイテムID

    Returns:
        found_item: 取得したアイテム
    """

    found_item = item_cruds.find_by_id(db, id, user.user_id)
    if not found_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return found_item


@router.get("/", response_model=List[ItemResponse], status_code=status.HTTP_200_OK)
async def find_by_name(
    db: DbDependency, name: str = Query(min_length=1, max_length=20)
):
    """
    指定した名前のアイテムを部分一致で取得します。

    Args:
        db (DbDependency): データベースセッションの依存関係
        name (str): アイテム名

    Returns:
        found_item: 取得したアイテム
    """

    found_item = item_cruds.find_by_name(db, name)
    if not found_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return found_item


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create(db: DbDependency, user: UserDependency, create_item: ItemCreate):
    """
    アイテムを新規作成します。

    Args:
        db (DbDependency): データベースセッションの依存関係
        create_item (ItemCreate): 作成するアイテムのデータ

    Returns:
        ItemResponse: 作成したアイテム
    """

    return item_cruds.create(db, create_item, user.user_id)


@router.post(
    "/multiple",
    response_model=List[ItemMessageResponse],
    status_code=status.HTTP_200_OK,
)
async def message_multiple(ids: List[ItemMessage], db: DbDependency, request: Request):
    """
    複数アイテムIDを疎通します。

    Args:
        db (DbDependency): データベースセッションの依存関係
        request (Request): FastAPIのリクエストオブジェクト

    Returns:
        ItemMessageResponse: 疎通したアイテム
    """

    req_ids = []
    for id in ids:
        req_ids.append(id.id)

    return item_cruds.message_multiple(db, req_ids)


@router.put("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def update(
    db: DbDependency,
    user: UserDependency,
    update_item: ItemUpdate,
    id: int = Path(gt=0),
):
    """
    指定したIDのアイテムを更新します。

    Args:
        db (DbDependency): データベースセッションの依存関係
        update_item (ItemUpdate): 更新するアイテムのデータ
        id (int): アイテムID

    Returns:
        updated_item: 更新したアイテム
    """

    updated_item = item_cruds.update(db, id, update_item, user.user_id)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not updated")
    return updated_item


@router.delete("/{id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
async def delete(db: DbDependency, user: UserDependency, id: int = Path(gt=0)):
    """
    指定したIDのアイテムを削除します。

    Args:
        db (DbDependency): データベースセッションの依存関係
        id (int): アイテムID

    Returns:
        deleted_item: 削除したアイテム
    """

    deleted_item = item_cruds.delete(db, id, user.user_id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not deleted")
    return deleted_item
