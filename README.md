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

### Dockerfileを使用した起動

Dockerfileを使用してコンテナをビルドし、実行します。

このプロジェクトはFastAPIを使用しています。FastAPIは、Python3.6+のための、現代的で、高速（高性能）なWebフレームワークです。

```bash:
docker build -t fastapi-app .
docker run -d --name fastapi-app -p 8000:8000 fastapi-app
```

### docker-compose.ymlを使用した起動

`docker-compose.yml`ファイルを使用して、サービスを起動します。

```bash:
docker-compose up -d
```

### 直接起動

`main.py`を直接実行することで、アプリケーションを起動できます。

```bash:
uvicorn main:app --reload
```

## 使用方法

上記コマンドによる起動後、`http://0.0.0.0:8000/`でアプリケーションにアクセスできます。  

アプリケーションが起動したら、`/docs`にアクセスして、Swagger UI を介して API を探索できます。  
また、`/redoc`で ReDoc を使用して API ドキュメントを見ることもできます。

## DBマイグレーション

- コンテナ起動の場合

1. appコンテナに入る
```bash:
docker-compose exec app sh
```

2. DBマイグレーション環境の作成

```bash:
alembic init migrations
sudo chown -R $(whoami):$(whoami) migrations/ alembic.ini
```

3. alembic.iniの修正

```ini:
sqlalchemy.url = postgresql://postgres:postgres@postgres:5432/admin
# connection local
# sqlalchemy.url = postgresql://postgres:postgres@localhost:25432/admin
```

4. migrations/env.pyの修正。

```python: env.py
from models import Base

target_metadata = Base.metadata
```

5. マイグレーションコマンドの実行。

```bash:
 alembic revision --autogenerate -m "Create items table"
```

6. マイグレーションの適用。

```bash:
alembic upgrade head
```


- ローカル起動の場合

1. DBマイグレーション環境の作成

```bash:
alembic init migrations
```

2. alembic.iniのsqlalchemy.urlを実際の環境に合わせる。

```ini: alembic.ini
sqlalchemy.url = postgresql://postgres:postgres@localhost:25432/admin
```

3. migrations/env.pyの修正。

```python: env.py
from models import Base

target_metadata = Base.metadata
```

4. マイグレーションコマンドの実行。

```bash:
 alembic revision --autogenerate -m "Create items table"
```

5. マイグレーションの適用。

```bash:
alembic upgrade head
```



## pgadminの接続

- General
  - 名前: admin
- 接続
  - ホスト名/アドレス: postgres
  - ポート番号: 5432
  - ユーザ名: postgres
  - パスワード: postgres

## requirements.txtを変更した場合

1. dockerを停止する。
```bash:
docker-compose stop
docker-compose rm -f
```

2. コンテナを起動する。
```bash:
docker-compose up -d
```

