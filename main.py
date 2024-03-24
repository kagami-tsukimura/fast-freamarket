from fastapi import Body, FastAPI

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


@app.post("/items")
async def create(create_item=Body(...)):
    """
    アイテムを新規登録します。
    """

    return item_cruds.create(create_item)


@app.put("/items/{id}")
async def update(id: int, update_item=Body(...)):
    """
    アイテムを更新します。
    """

    return item_cruds.update(id, update_item)


@app.delete("/items/{id}")
async def delete(id: int):
    """
    アイテムを削除します。
    """

    return item_cruds.delete(id)
