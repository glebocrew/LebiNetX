from fastapi import FastAPI
from _api.routers import UserRouter, PostRouter

app = FastAPI()
app.include_router(UserRouter)
app.include_router(PostRouter)
# db = DataBase()


@app.get("/")
async def index():
    return {"test_message": "If you see this, Gleb. FastAPI works."}
