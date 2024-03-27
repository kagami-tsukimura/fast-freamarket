import base64
import hashlib
import os

from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate


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
