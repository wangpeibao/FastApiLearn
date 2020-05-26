from typing import List

import uvicorn
from fastapi import FastAPI, Cookie, Header
from pydantic import BaseModel

app = FastAPI()


@app.get("/request01")
def request01(*, val: str = Cookie(...)):
    return val

@app.get("/request02")
def request02(*, val: str = Header(...)):
    return val

@app.get("/request03")
def request03(*, val_item: str = Header(...)):
    return val_item

@app.get("/request04")
def request04(*, val_list: List[str] = Header(...)):
    return val_list


class Item(BaseModel):
    name: str
    age: int = 18

@app.post("/request05", response_model=Item)
def request05(*, item: Item):
    return item

@app.post("/request06", response_model=List[Item])
def request06(*, item: Item):
    return [item, item]

class OutItem(BaseModel):
    name: str

@app.post("/request07", response_model=OutItem)
def request07(*, item: Item):
    return item

@app.post("/request08", response_model=Item, response_model_exclude_unset=True)
def request08(*, item: Item):
    return item

@app.post("/request09", response_model=Item, response_model_include={"name"})
def request09(*, item: Item):
    return item

@app.post("/request10", response_model=Item, response_model_exclude={"age"})
def request10(*, item: Item):
    return item

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)