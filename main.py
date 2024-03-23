from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/")
async def read_item():
    return {"item": "item1", "q": "q"}


@app.get("/example/")
async def example():
    return {"example": "example1"}
