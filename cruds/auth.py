import base64
import hashlib
import os
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from models import User
from schemas import DecodedToken, UserCreate

ALGORITHM = "HS256"
SECRET_KEY = "d71afefe71224d864f67b71cd9d3d91ad709ef6bd6eaa3e6166d2f4d1f4f37ab"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_user(db: Session, user_create: UserCreate):
    salt = base64.b64encode(os.urandom(32))
    # パスワードのハッシュ化

    # ハッシュアルゴリズム: SHA-256
    # パスワード: user_create.password
    # パスワードに追加するバイト: salt
    # 繰り返し: 1000
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", user_create.password.encode(), salt, 1000
    ).hex()

    new_user = User(
        username=user_create.username, password=hashed_password, salt=salt.decode()
    )
    db.add(new_user)
    db.commit()

    return new_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    # early return
    if not user:
        return None

    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), user.salt.encode(), 1000
    ).hex()

    return user if user.password == hashed_password else None


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    expires = datetime.now() + expires_delta
    payload = {"sub": username, "id": user_id, "exp": expires}

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")

        return (
            DecodedToken(username=username, user_id=user_id)
            if username and user_id
            else None
        )

    except JWTError:
        raise JWTError
