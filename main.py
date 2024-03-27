import uvicorn
from fastapi import FastAPI

from routers import auth, item

app = FastAPI()
app.include_router(item.router)
app.include_router(auth.router)


@app.get("/")
async def example():
    """
    起動確認としてHello Worldを返します。
    """

    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
