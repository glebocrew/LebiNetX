from fastapi import routing
from _db import DataBase
from _api.response_models import PostReaction, CommentReaction
from typing import List, Tuple

reaction_router = routing.APIRouter()

db = DataBase()


@reaction_router.post("/reactions")
async def create_reaction(
    type: str, userId: str, objectId: str, reaction: int
) -> Tuple[str, int]:
    if type == "post_reaction":
        message, status = db.create_post_reaction(
            userId=userId, postId=objectId, reaction=reaction
        )
        return message, status
    if type == "comment_reaction":
        message, status = db.create_comment_reaction(
            userId=userId, commentId=objectId, reaction=reaction
        )
        return message, status
    else:
        return "No type selected", 400


@reaction_router.get("/reactions")
async def reactions(type: str, postId: str) -> List[PostReaction]:
    if type == "post_reaction":
        post_reactions_raw = db.get_post_reactions(postId)
        if post_reactions_raw is None:
            return None
        else:
            posts = []
            for post in post_reactions_raw:
                posts.append(PostReaction(**post))
            return posts
    if type == "comment_reaction":
        post_reactions_raw = db.get_post_reactions(postId)
        if post_reactions_raw is None:
            return None
        else:
            reactions = []
            for reaction in post_reactions_raw:
                reactions.append(CommentReaction(**reaction))
            return posts
    else:
        return []


@reaction_router.delete("/reactions")
async def delete_reactions(type: str, objectId: str) -> int:
    if type == "post_reaction":
        response = db.delete_post_reaction(postId=objectId)
    if type == "comment_reaction":
        response = db.delete_comment_reaction(postId=objectId)
    else:
        return 400

    return response
