from fastapi import FastAPI
import uvicorn

app = FastAPI()  # 创建应用实例，uvicorn启动时也基于这个实例


@app.get("/")  # 定义了一个"/"根目录的路由，直接返回了一个字符串
async def hello_world():
    return "Hello World"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, headers=[("author", "wangpeibao")])
