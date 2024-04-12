"""
conftest.py
    pytest実行時に自動で読み込むファイル
    テストコード共通の設定や処理を定義
    e.g. DBセットアップ
"""

# flake8: noqa: E402
import os
import sys

parent_dir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(parent_dir)


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from cruds.auth import get_current_user
from database import get_db
from main import app
from models import Base, Item, ItemSub
from schemas import DecodedToken

"""
fixture: 
    pytestにおけるテストコードの前処理。
    データのセットアップやクリーンアップなど。
"""

"""
@pytest.fixture: 
    このデコレータを付与した関数をfixture関数として扱う
"""


@pytest.fixture
def session_fixture():
    # テスト用のSQLiteでDBセッションを作成
    engine = create_engine(
        # 別スレッド可、静的プールでスレッドセーフなDBアクセス
        url="sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # テーブル作成
    # NOTE: DBエンジンを渡すことで、Baseを継承するテーブルを一括でCREATEする
    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()

    try:
        # テスト用にItemを2つ登録
        item1 = Item(name="PC1", price=10000, description="test1", user_id="1")
        item2 = Item(name="PC2", price=20000, description="test2", user_id="2")
        # テスト用にItemSubを2つ登録
        item_sub1 = ItemSub(name="PC1")
        item_sub2 = ItemSub(name="PC2")
        db.add(item1)
        db.add(item2)
        db.add(item_sub1)
        db.add(item_sub2)
        db.commit()
        # yield以前の処理がpytestの前処理
        yield db
        # yieldより後の処理がpytestの後処理
    finally:
        db.close()


@pytest.fixture()
def user_fixture():
    # テスト用のユーザーデータを返却
    return DecodedToken(username="user1", user_id=1)


@pytest.fixture()
def client_fixture(session_fixture: Session, user_fixture: DecodedToken):
    # テストクライアントのセットアップ
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
