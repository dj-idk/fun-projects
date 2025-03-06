from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn

from database import init_db
from router import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan, title="Simple Blog API")

app.include_router(post_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
