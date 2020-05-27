from typing import List, Union, Dict

import uvicorn
from fastapi import FastAPI, Cookie, Header, Form, File, UploadFile
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

class Item1(BaseModel):
    name: str
    age: int = 1

class Item2(BaseModel):
    name: str
    age: int
    alias_name: str = "别名"

class Item3(Item1):
    alias_name: str = "别名"

class Item4(BaseModel):
    alias_name: str = "别名"

@app.post("/request11")
def request11(*, item: Item1):
    print(item.dict())
    item2 = Item2(**item.dict())
    return item2

@app.post("/request12")
def request12(*, item: Item1):
    item3 = Item3(**item.dict(), alias_name="哈哈")
    return item3

@app.post("/request13", response_model=Union[Item1, Item4])
def request13(*, item: Item1):
    return item

@app.post("/request14", response_model=Dict[str, int])
def reqeust14():
    return {"a": 1, "b": 2}

@app.post("/request15")
def request15(name: str = Form(...)):
    return name

@app.post("/request16")
def request16(file: bytes = File(...)):
    return len(file)

@app.post("/request17")
async def request17(file: UploadFile = File(...)):
    with open("./%s" % file.filename, "wb") as f:
        content = await file.read()
        f.write(content)
        f.close()
    return file.filename

@app.post("/reqeust18")
def request18(files: List[UploadFile] = File(...)):
    res = []
    for file in files:
        res.append(file.filename)
    return res


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)