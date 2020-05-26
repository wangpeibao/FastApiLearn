import uvicorn
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

class Item1(BaseModel):
    name: str

class Item2(BaseModel):
    name: str

@app.post('/request_body01')
def request_body01(*, item1: Item1, item2: Item2):
    return [item1, item2]

@app.post("/request_body02")
def request_body02(*, item1: Item1, item2: Item2, item3: str = Body(...)):
    return [item1, item2, item3]

@app.post("/request_body03")
def request_body03(item1: Item1 = Body(..., embed=True)):
    return item1

class Item3(BaseModel):
    name: str = Field(..., min_length=3)
    age: int = Field(..., ge=0)

@app.post("/request_body04")
def request_body04(item: Item3):
    return item

from typing import List, Set, Dict, FrozenSet


class Item4(BaseModel):
    list1: list = []
    list2: List = []
    list3: List[int] = [1]

class Item5(BaseModel):
    set1: set = set()
    set2: Set = set()
    set3: Set[str] = set()
    list1: Item4 = None
    list2: List[Item4] = None

@app.post("/request_body05")
def request_body05(item: Item5):
    return item

@app.post("/request_body06")
def reuqest_body06(item: List[Item1]):
    return item

@app.post("/request_body07")
def reuqest_body07(dict1: Dict[str, int]):
    return dict1

class Item6(BaseModel):
    name: str = Field(..., example="wang")
    age: int = Field(..., example=1)

class Item7(BaseModel):
    sex: int

    class Config:
        schema_extra = {
            "example": {"sex": 1}
        }

@app.post("/request_body08")
def request_body08(item1: Item6, item2: Item7):
    return [item1, item2]

from uuid import UUID
import datetime

class Item8(BaseModel):
    # object_id: UUID
    # datetime1: datetime.datetime
    # date1: datetime.date
    # time1: datetime.time
    # timedelta1: datetime.timedelta
    frozenset1: frozenset = None
    byte1: bytes = None

@app.post("/request_body09")
def request_body09(item: Item8):
    # print((item.datetime1 + item.timedelta1).strftime("%Y-%m-%d %H:%M:%S"))
    print(item)
    return item


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)