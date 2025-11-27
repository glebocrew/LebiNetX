from fastapi import FastAPI
from _api.response_models import User
from typing import List, Optional, Tuple
from _db import DataBase

app = FastAPI()
db = DataBase()


@app.get("/")
async def index():
    return {"test_message": "If you see this, Gleb. FastAPI works."}


@app.get("/users")
async def users() -> Optional[List[User]]:
    users_raw = db.get_users()
    if users_raw is None:
        return None

    users = []
    for user in users_raw:
        temp_user = User(**user)
        users.append(temp_user)

    return users


@app.get("/user")
async def user(
    userId: Optional[str] = None,
    email: Optional[str] = None,
    nickname: Optional[str] = None,
) -> Optional[User]:
    user_raw = db.get_user(userId=userId, email=email, nickname=nickname)
    print(f"USER: {user_raw}")

    if user_raw is None:
        return None

    user = User(**user_raw)

    return user


@app.delete("/user")
def delete_user(userId: str) -> int:
    response = db.delete_user(userId)
    return response


@app.post("/user")
def create_user(email: str, nickname: str) -> Tuple[str, int]:
    message, response = db.create_user(email=email, nickname=nickname)
    if response == 200:
        return (
            "",
            200,
        )
    else:
        return (str(message).split(sep=":")[0], response)

    # who never ever reads this text is gay except for the creator and me
