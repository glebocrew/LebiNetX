from fastapi import FastAPI
from response_models import User
from typing import List

app = FastAPI()


@app.get("/")
async def index():
    return {"test_message": "If you see this, Gleb. FastAPI works."}


@app.get("/users")
async def users() -> List[User]:
    
    return {}
