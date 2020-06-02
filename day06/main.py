from datetime import datetime
from typing import FrozenSet

import uvicorn
from fastapi import FastAPI, Depends, Header, Query, Request, BackgroundTasks
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="1", description="2", version="3", docs_url="/mydoc")


async def pagination(page_num: int = 1, page_count: int = 10):
    # 转化成页码的范围
    return {"page_start": (page_num - 1) * page_count, "page_end": page_num * page_count - 1}

@app.get("/request01")
async def request01(*, page: dict = Depends(pagination), c: int):
    return [page, c]


class Pagination:
    def __init__(self, page_num: int = 1, page_count: int = 10):
        self.page_start = (page_num - 1) * page_count
        self.page_end = page_num * page_count - 1

@app.get("/request02")
async def request02(*, page: Pagination = Depends(Pagination)):
    return page

async def pagination1(page: dict = Depends(pagination), other: int = 0):
    page.update({"other": other})
    return page

@app.get("/request03")
async def request03(page: dict = Depends(pagination1)):
    return page

async def verify_header(token: str = Header(...)):
    print(token)

async def verify_query(name: str = Query(...)):
    print(name)

@app.get("/request04", dependencies=[Depends(verify_header), Depends(verify_query)])
def request04():
    return "hello world"

# 中间件简介
@app.middleware("http")
async def get_response_time(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    end_time = datetime.now()
    print(end_time.timestamp() - start_time.timestamp())
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import time

# 后台任务
def bktask():
    for i in range(10):
        print(i)
        time.sleep(2)

@app.get("/request05")
def request05(backtask: BackgroundTasks):
    backtask.add_task(bktask)
    return "hello world"


class Model(BaseModel):
    b: FrozenSet = frozenset({1, 2, 3})
    c: frozenset = frozenset({1, 2, 3})
    d: frozenset = ...

print(Model.schema())

app.mount("/static", StaticFiles(directory="static"), name="123")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)