import os
import sys

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from cruds.auth import get_current_user
from database import get_db
from main import app
from models import Base, Item
from schemas import DecodedToken

parent_dir = os.path.dirname(os.path.dirname(__file__), "..")
sys.path.append(parent_dir)


@pytest.fixture()
def session_fixture():
    engine = create_engine(
        url="sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        item1 = Item(name="PC1", price=10000, description="test1", user_id="1")
        item2 = Item(name="PC2", price=20000, description="test2", user_id="2")
        db.add(item1)
        db.add(item2)
        db.commit()
        yield db
    finally:
        db.close()


@pytest.fixture()
def user_fixture():
    return DecodedToken(username="user1", user_id=1)


@pytest.fixture()
def client_fixture(session_fixture: Session, user_fixture: DecodedToken):
    def override_get_db():
        return session_fixture

    def override_get_current_user():
        return user_fixture

    # テスト用の依存関係をオーバーライド
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)
    yield client

    # 依存関係をクリア
    app.dependency_overrides.clear()
