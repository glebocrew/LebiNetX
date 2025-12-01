from fastapi import routing
from _api.response_models import Comment
from _db.orm_ops import DataBase
from typing import List, Tuple


comment_router = routing.APIRouter()
db = DataBase()


@comment_router.get("/comments")
async def comments(postId: str = None) -> List[Comment]:
    if postId is not None:
        comments_raw = db.get_comments(postId)
        if comments_raw is None:
            return None
        else:
            comments = []
            for comment in comments_raw:
                comments.append(comment(**Comment))
            return comments


@comment_router.post("/comments")
async def new_comment(userId: str, postId: str, content: str) -> Tuple[str, int]:
    message, status = db.create_comment(userId=userId, postId=postId, content=content)

    return message, status
