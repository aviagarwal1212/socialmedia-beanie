from typing import List

from app.models.post import CreatePost, OutPost, Post, UpdatePost
from app.models.user import User
from app.models.vote import Vote
from app.utils import oauth2, pydantic_encoder
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Response, status

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[OutPost])
async def get_posts(current_user: User = Depends(oauth2.get_current_user)):
    posts = await Post.find(fetch_links=True).to_list()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
async def create_post(
    post_data: CreatePost, current_user: User = Depends(oauth2.get_current_user)
):
    post_data = Post(owner=current_user, **post_data.dict())
    post = await Post.insert_one(post_data)
    _ = await Vote.insert(Vote(id=post.id))
    return post


@router.get("/{id}", response_model=OutPost)
async def get_post(
    id: PydanticObjectId, current_user: User = Depends(oauth2.get_current_user)
):
    post = await Post.get(id, fetch_links=True)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: PydanticObjectId, current_user: User = Depends(oauth2.get_current_user)
):
    post = await Post.get(id, fetch_links=True)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    if post.owner != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )
    _ = await post.delete()
    _ = await Vote.get(id).delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=Post)
async def update_post(
    id: PydanticObjectId,
    post_data: UpdatePost,
    current_user: User = Depends(oauth2.get_current_user),
):
    post = await Post.get(id, fetch_links=True)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    if post.owner != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorized to perform requested action",
        )
    post_data = pydantic_encoder.encode_input(post_data)
    _ = await post.update({"$set": post_data})
    updated_post = await Post.get(id, fetch_links=True)
    return updated_post
