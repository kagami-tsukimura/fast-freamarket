from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from cruds import auth as auth_cruds
from database import get_db
from schemas import UserCreate, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

DbDependency = Annotated[Session, Depends(get_db)]


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(db: DbDependency, user_create: UserCreate):
    return auth_cruds.create_user(db, user_create)
