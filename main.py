import uvicorn
from fastapi import FastAPI

from routers import item as item_routers

app = FastAPI()
app.include_router(item_routers.router)


@app.get("/")
async def example():
    """
    起動確認としてHello Worldを返します。
    """

    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
