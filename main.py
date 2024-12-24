from fastapi import FastAPI
import uvicorn

from db import init_models
from contextlib import asynccontextmanager

from router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Включение")
    await init_models()
    print("База данных включилась")
    yield
    print("Выключение")

app = FastAPI(lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
