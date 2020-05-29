from datetime import datetime, date
from typing import List, Mapping, AbstractSet

import uvicorn
from fastapi import FastAPI, HTTPException, Request, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import HTTPException as SelfException
from pydantic import BaseModel, Field

app = FastAPI()


@app.get("/request01")
def request01():
    raise HTTPException(status_code=401, detail={"custom": "自定义数据类型"}, headers={"Err-Msg": "123"})
    return "hello world"

class MyException(Exception):
    def __init__(self, msg):
        self.msg = msg

@app.exception_handler(MyException)
async def my_exception_handler(request: Request, e: MyException):
    return JSONResponse(
        status_code=418,
        content={"message": f"{e.msg}", "data": 123},
    )

@app.get("/request02")
def request02():
    raise MyException(msg="123")
    return "hello world"

@app.exception_handler(RequestValidationError)
async def my_request_validation_exception(request: Request, e: RequestValidationError):
    # 解析RequestValidationError的数据，重新拼接返回
    rtype = e.raw_errors[0].loc_tuple()[0]
    rkey = e.raw_errors[0].loc_tuple()[1]
    msg = e.raw_errors[0].exc.msg_template
    return JSONResponse(
        status_code=418,
        content=[rtype, rkey, msg]
    )

@app.exception_handler(SelfException)
async def my_exception_handler1(request: Request, e: HTTPException):
    print("hello exception")
    return await http_exception_handler(request, e)

@app.get("/request03")
def request03(num: int = Query(...)):
    return "hello world"


@app.get("/request04", status_code=status.HTTP_401_UNAUTHORIZED, tags=["request"], summary="1", description="1",
         response_description="1", deprecated=True)
def request04():
    return "hello world"


class Item(BaseModel):
    a: datetime = Field(None, alias="aa")
    b: date = Field(None)
    c: int = Field(1)
    d: str
    e: bool

@app.post("/request05")
def request05(item: Item):
    item1 = jsonable_encoder(item)
    print(type(item1))
    return item

@app.post("/request06")
def request06(item: List[Item]):
    item1 = jsonable_encoder(item)
    print(type(item1))
    return item

@app.post("/request07")
def request07(item: Item):
    print(item.dict(by_alias=True))
    print(item.dict(exclude_unset=True))
    print(item.dict(exclude_none=True))
    print(item.dict(exclude_defaults=True))
    print(item.dict(exclude={"c", "d"}))
    # copy方法
    item1 = {"d": 1993}
    print(item1)
    item2 = item.copy(update=item1, deep=True)
    return item2



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)