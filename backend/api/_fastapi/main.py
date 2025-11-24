from fastapi import FastAPI

app = FastAPI()

app.get("/")
async def index():
    return {
        "test_message": "If you see this, Gleb. FastAPI works."
    }