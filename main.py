from fastapi import FastAPI
from contextlib import asynccontextmanager

from pydantic import BaseModel

items = {}
local_greetings = {"en": "Good Day", "dk":"Hejsa", "se":"Tja", "no": "Hei", "fi":"Moikka"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Start up')
    items["greeting"] = "Hello"
    yield
    print('Shut down')


app = FastAPI(lifespan=lifespan)

class GreetRequest(BaseModel):
    name: str

@app.get("/greet")
async def greet():
    return {"data": items["greeting"]}

@app.get("/greet/{country_code}")
async def greet(country_code):
    return {"data": local_greetings[country_code]}


@app.post("/greet")
async def greet(request: GreetRequest):
    return {"data": f"Hello, {request.name}"}