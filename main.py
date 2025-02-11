from fastapi import FastAPI
from contextlib import asynccontextmanager
import debugpy
from pydantic import BaseModel
import uvicorn

items = {}
local_greetings = {"en": "Good Day", "dk":"Hejsa", "se":"Tja", "no": "Hei", "fi":"Moikka"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('Start up')
    items["greeting"] = "Hello"
    yield {"stuff": "Heya"}
    print('Shut down')


app = FastAPI(lifespan=lifespan, debug=True)


class GreetRequest(BaseModel):
    name: str

@app.get("/greet")
async def greet():
    return {"data": items["greeting"]}

@app.get("/greet/local/{country_code}")
async def greet(country_code):
    return {"data": local_greetings[country_code]}


@app.post("/greet")
async def greet(request: GreetRequest):
    return {"data": f"Hello, Sir {request.name}"}


@app.get("/greet/personal/")
async def greet(country_code: str=None, name: str=None):
    if country_code and name:
        return f"{local_greetings[country_code]}, {name}"
    elif country_code:
        return f"{local_greetings[country_code]}"
    elif name:
        return f"Heya, {name}"
    else:
        return "Sup bro?"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug")

    debugpy.listen(("0.0.0.0", 5678))
    print("Waiting for debugger to attach...")
    debugpy.wait_for_client()
    print("Debugged attached")