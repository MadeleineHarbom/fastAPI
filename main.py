from fastapi import FastAPI
from contextlib import asynccontextmanager
import debugpy
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

debugpy.listen(("0.0.0.0", 5678))
print("Waiting for debugger to attach...")
debugpy.wait_for_client()
print("Debugged attached")


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug")