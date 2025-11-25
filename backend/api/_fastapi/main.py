from fastapi import FastAPI
from _fastapi.response_models import User
from typing import List
from mariadb import DataBase

app = FastAPI()
db = DataBase()

@app.get("/")
async def index():
    return {"test_message": "If you see this, Gleb. FastAPI works."}


@app.get("/users")
async def users() -> List[User]:
    users_raw = db.get_users()
    if users_raw != -1:
        return users
    else:
        return -1
