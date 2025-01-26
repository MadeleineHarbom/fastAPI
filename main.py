from fastapi import FastAPI
from contextlib import asynccontextmanager

items = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Start up')
    items["greeting"] = "Hello"
    yield
    print('Shut down')


app = FastAPI(lifespan=lifespan)


@app.get("/greet")
async def greet():
    return {"result": items["greeting"]}