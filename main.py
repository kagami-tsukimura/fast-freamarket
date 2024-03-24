from fastapi import FastAPI

from cruds import item as item_cruds

app = FastAPI()


@app.get("/")
async def example():
    """
    起動確認としてHello Worldを返します。
    """
    return {"message": "Hello World"}


@app.get("/items")
async def find_all():
    """
    全てのアイテムを取得します。
    """
    return item_cruds.find_all()


@app.get("/items/{id}")
async def find_by_id(id: int):
    """
    指定したIDのアイテムを取得します。
    """
    return item_cruds.find_by_id(id)


@app.get("/items/")
async def find_by_name(name: str):
    """
    指定した名前のアイテムを部分一致で取得します。
    """
    return item_cruds.find_by_name(name)
