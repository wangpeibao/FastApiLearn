import uvicorn
from fastapi import FastAPI, Depends

app = FastAPI()


async def pagination(page_num: int = 1, page_count: int = 10):
    # 转化成页码的范围
    return {"page_start": (page_num - 1) * page_count, "page_end": page_num * page_count - 1}

@app.get("/request01")
async def request01(*, page: dict = Depends(pagination), c: int):
    return [page, c]

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)