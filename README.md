# FastAPI プロジェクト

このプロジェクトはFastAPIを使用したサンプルアプリケーションです。

## 必要条件

- Python 3.11+
- FastAPI
- Uvicorn: FastAPIを実行するためのASGIサーバ

## インストール方法

依存関係をインストールするには、以下のコマンドを実行してください。

```bash:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 起動方法

### docker-compose.ymlを使用した起動

`docker-compose.yml`ファイルを使用して、サービスを起動します。
初回のみ、`--build`をつけて実行してください。

```bash:
docker-compose up -d --build
```

2回目以降。
```bash:
docker-compose up -d
```

<details><summary>Dockerfileを使用した起動</summary>
Dockerfileを使用してコンテナをビルドし、実行します。  

このプロジェクトはFastAPIを使用しています。  

```bash:
docker build -t fastapi-app .
docker run -d --name fastapi-app -p 8000:8000 fastapi-app
```
</details>

<details><summary>直接起動</summary>
`main.py`を直接実行することで、アプリケーションを起動できます。

```bash:
uvicorn main:app --reload
```
</details>

## 使用方法

コンテナ起動後、`http://0.0.0.0:8000/`でアプリケーションにアクセスできます。  

アプリケーションが起動したら、`/docs`にアクセスして、Swagger UI を介して API を探索できます。  
また、`/redoc`で ReDoc を使用して API ドキュメントを見ることもできます。

## DBマイグレーション

コンテナ起動後、下記の手順でマイグレーションを実装する。  
コンテナに構築したFastAPI環境内での実行を想定。

1. appコンテナに入る

```bash:
docker-compose exec app /bin/bash
```

2. DBマイグレーション環境の作成

```bash:
alembic init migrations
sudo chown -R $(whoami):$(whoami) migrations/ alembic.ini
```

3. alembic.iniの修正

```ini:
sqlalchemy.url = postgresql://postgres:postgres@postgres:5432/admin
```

4. migrations/env.pyの修正。

```python: env.py
from models import Base

target_metadata = Base.metadata
```

5. マイグレーションコマンドの実行。

```bash:
alembic revision --autogenerate -m "Create table"
```

6. マイグレーションの適用。

```bash:
alembic upgrade head
```

## pgadminの接続

ログイン情報は、`docker-compose.yml`に記載しています。  
接続情報は、下記を参照してください。  

- General
  - 名前: admin
- 接続
  - ホスト名/アドレス: postgres
  - ポート番号: 5432
  - ユーザ名: postgres
  - パスワード: postgres

## requirements.txtを変更した場合

1. dockerを終了する。
```bash:
docker-compose down -v
```

2. コンテナを起動する。
```bash:
docker-compose up -d
```

## 秘密鍵の作成

1. opensslコマンドを実行する。

```bash:
openssl rand -hex 32
```

2. opensslコマンドで返ってきた値を使用する。
