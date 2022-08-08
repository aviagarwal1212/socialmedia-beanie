from typing import List

from app.models.post import CreatePost, OutPost, Post, UpdatePost
from app.models.user import User
from app.utils import oauth2, pydantic_encoder
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, Response, status

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[OutPost])
async def get_posts(current_user: User = Depends(oauth2.get_current_user)):
    posts = await Post.find_all().to_list()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OutPost)
async def create_post(
    post_data: CreatePost, current_user: User = Depends(oauth2.get_current_user)
):
    post_data = Post(owner_id=current_user.id, **post_data.dict())
    post = await Post.insert_one(post_data)
    return post


@router.get("/{id}", response_model=OutPost)
async def get_post(
    id: PydanticObjectId, current_user: User = Depends(oauth2.get_current_user)
):
    post = await Post.get(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    id: PydanticObjectId, current_user: User = Depends(oauth2.get_current_user)
):
    post = await Post.get(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    _ = await post.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=OutPost)
async def update_post(
    id: PydanticObjectId,
    post_data: UpdatePost,
    current_user: User = Depends(oauth2.get_current_user),
):
    post = await Post.get(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    post_data = pydantic_encoder.encode_input(post_data)
    _ = await post.update({"$set": post_data})
    updated_post = await Post.get(id)
    return updated_post
