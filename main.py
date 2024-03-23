from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def example():
    return {"message": "Hello World"}


@app.get("/items/")
async def read_item():
    return {"item": "item1", "q": "q"}
