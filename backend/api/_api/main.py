from fastapi import FastAPI
from _api.routers import UserRouter, PostRouter, ReactionRouter, CommentRouter

app = FastAPI()
app.include_router(UserRouter)
app.include_router(PostRouter)
app.include_router(ReactionRouter)
app.include_router(CommentRouter)
# db = DataBase()


@app.get("/")
async def index():
    return {"test_message": "If you see this, Gleb. FastAPI works."}
