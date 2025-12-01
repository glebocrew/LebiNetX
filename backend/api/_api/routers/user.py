from fastapi import routing
from typing import Optional, List, Tuple
from _api.response_models import User
from _db import DataBase

db = DataBase()

user_router = routing.APIRouter()


@user_router.get("/users")
async def users() -> Optional[List[User]]:
    users_raw = db.get_users()
    if users_raw is None:
        return None

    users = []
    for user in users_raw:
        temp_user = User(**user)
        users.append(temp_user)

    return users


@user_router.get("/user")
async def user(
    userId: Optional[str] = None,
    email: Optional[str] = None,
    nickname: Optional[str] = None,
) -> Optional[User]:
    user_raw = db.get_user(userId=userId, email=email, nickname=nickname)
    # print(f"USER: {user_raw}")

    if user_raw is None:
        return None

    user = User(**user_raw)

    return user


@user_router.delete("/user")
def delete_user(userId: str) -> int:
    response = db.delete_user(userId)
    return response


@user_router.post("/user")
def create_user(email: str, nickname: str, password: str) -> Tuple[str, int]:
    message, response = db.create_user(email=email, nickname=nickname, pwd=password)

    return (message, response)

    # who never ever reads this text is gay except for the creator and me


@user_router.patch("/user")
def patch_user(
    userId: str,
    email: Optional[str] = None,
    nickname: Optional[str] = None,
    password: Optional[str] = None,
) -> Tuple:
    # print(db.patch_user(userId=userId, email=email, nickname=nickname, password=password))
    message, response = db.patch_user(
        userId=userId, email=email, nickname=nickname, password=password
    )
    if response == 200:
        return (
            "",
            200,
        )
    else:
        return (message, response)
