from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config.database import init_db
from .routers import auth, post, user, vote

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start_db():
    await init_db()


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to my socialmedia-beanie API."}
