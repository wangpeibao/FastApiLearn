from typing import List

import uvicorn
from fastapi import FastAPI
from enum import Enum
app = FastAPI()


@app.get("/param_get1/{param}")  # 以大括号包裹，默认是字符串类型，在路径中获取参数
def param_get1(param):
    return {"param": param}


@app.get("/param_get2/{param}")  # 可以指定数据类型，会进行数据类型转化
def param_get2(param: int):
    return {"param": param}


@app.get("/param_get3/me")
def param_get3():
    return {"param": "me"}


@app.get("/param_get3/{param}")
def param_get4(param):
    return {"param": param}


class items(Enum):
    a = "a"
    b = "b"
    c = "c"


@app.get("/param_get5/{param}")
def param_get5(param: items):
    return {"param": param}


@app.get("/param_get6/{file_path: path}")
def param_get6(file_path):
    return {"file_path": file_path}


# query param
@app.get("/param_query1")
def param_query1(a, b):  # 默认是str类型
    return [a, b]


@app.get("/param_query2")
def param_query2(a: int, b: float):  # 声明数据类型
    return [a, b]


@app.get("/param_query3")
def param_query3(a: int = 1, b: float = 2.3):  # 给参数声明了默认值
    return [a, b]

# request body param


from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int = 18


@app.post("/param_request_body1")
def param_request_body1(user: User):
    return user

# 数据校验
from fastapi import Query, Path

@app.get("/param_validate1/{item}")
def param_validate1(item: int = Path(1, description = "描述", ge = 10)):
    return {"item": item}

@app.get("/param_validate2")
def param_validate2(item: int = Query(1, description = "query参数", le = 10)):
    return {"item": item}

@app.get("/param_validate3")
def param_validate3(item: int = Query(..., description = "query参数", le = 10)):
    return {"item": item}

@app.get("/param_validate4")
def param_validate4(item: str = Query(..., description="字符串长度限制", min_length = 3)):
    return {"item": item}

@app.get("/param_validate5")
def param_validate5(item: str = Query(..., description="正则表达式", regex=r"[0-7]+")):
    return {"item": item}

@app.get("/param_validate6")
def param_validate6(item: List[str] = Query(None)):
    return {"item": item}

@app.get("/param_validate7")
def param_validate7(item: List[str] = Query(["a", "b"])):
    return {"item": item}

# @app.get("/param_validate8")
# def param_validate8(t1: str = None, t2: str):
#     return [t1, t2]

@app.get("/param_validate9")
def param_validate9(*, t1: str = None, t2: str):
    return [t1, t2]

@app.get("/param_validate10")
def param_validate10(t1: str = None, t2: str = Query(...)):
    return [t1, t2]


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
