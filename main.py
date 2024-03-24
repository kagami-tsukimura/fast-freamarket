from fastapi import FastAPI

from cruds import item as item_cruds

app = FastAPI()


@app.get("/")
async def example():
    return {"message": "Hello World"}


@app.get("/items/")
async def find_all():
    return item_cruds.find_all()


@app.get("/items/{item_id}")
async def find_by_id(item_id: int):
    return item_cruds.find_by_id(item_id)
