from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate


def create_user(db: Session, user_create: UserCreate):
    new_user = User(**user_create.model_dump())
    db.add(new_user)
    db.commit()

    return new_user
