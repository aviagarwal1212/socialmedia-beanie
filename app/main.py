from fastapi import FastAPI

from .config.database import init_db
from .routers import auth, post, user

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.on_event("startup")
async def start_db():
    await init_db()


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to my socialmedia-beanie API."}
