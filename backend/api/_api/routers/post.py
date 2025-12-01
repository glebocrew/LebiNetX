from fastapi import routing
from _db import DataBase
from _api.response_models import Post, Hashtag
from typing import Optional, List, Tuple

post_router = routing.APIRouter()
db = DataBase()


@post_router.get("/posts")
async def posts(userId: Optional[str] = None) -> Optional[List[Post]]:
    if userId is not None:
        posts_raw = db.get_user_posts(userId)
        if posts_raw is None:
            return None
        else:
            posts = []
            for post in posts_raw:
                posts.append(Post(**post))
            return posts

    if userId is None:
        posts_raw = db.get_posts()
        # print(posts_raw)
        if posts_raw is None:
            return None

        posts = []
        for post in posts_raw:
            posts.append(Post(**post))

        return posts


@post_router.post("/posts")
async def new_post(userId: str, title: str, content: str) -> Tuple[str, int]:
    message, status = db.create_post(userId=userId, title=title, content=content)

    return message, status


@post_router.delete("/posts")
async def delete_post(postId: str) -> int:
    response = db.delete_post(postId=postId)
    return response


@post_router.patch("/posts")
async def patch_user(
    postId: str, title: Optional[str] = None, content: Optional[str] = None
) -> Tuple:
    # print(db.patch_user(userId=userId, email=email, nickname=nickname, password=password))
    message, response = db.patch_post(postId=postId, title=title, content=content)

    if response == 200:
        return (
            "",
            200,
        )
    else:
        return (message, response)


@post_router.get("/hashtags")
async def hashtags(postId: str) -> List[Hashtag]:
    hashtags_raw = db.get_hashtags(postId)
    if hashtags_raw is None:
        return None
    else:
        hashtags = []
        for hashtag in hashtags_raw:
            hashtags.append(Hashtag(**hashtag))
        return hashtags
