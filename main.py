from time import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, item, item_sub

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # localhost:3000からの操作のみ許可
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# 処理時間計測ミドルウェア
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    # 処理の所要時間をレスポンスヘッダに記載
    process_time = time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


app.include_router(item.router)
app.include_router(auth.router)
app.include_router(item_sub.router)


@app.get("/")
async def example():
    """
    起動確認としてHello Worldを返します。
    """

    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
