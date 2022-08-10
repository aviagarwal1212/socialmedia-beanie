from typing import List

from app.models.post import Post
from app.models.user import OutUser, User
from app.models.vote import Vote
from app.utils import oauth2
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/{id}", status_code=status.HTTP_201_CREATED)
async def call_vote(
    id: PydanticObjectId, current_user: User = Depends(oauth2.get_current_user)
):
    post = await Post.get(id, fetch_links=True)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    vote = await Vote.get(id)
    current_votes = vote.users
    if current_user.id in current_votes:
        _ = await vote.update({"$pull": {"users": current_user.id}})
        _ = await post.update({"$inc": {"votes": -1}})
        return {"message": "successfully deleted vote"}
    else:
        _ = await vote.update({"$push": {"users": current_user.id}})
        _ = await post.update({"$inc": {"votes": 1}})
        return {"message": "successfully added vote"}


@router.get("/{id}", response_model=List[OutUser])
async def get_vote_users(
    id: PydanticObjectId, current_user: User = Depends(oauth2.get_current_user)
):
    vote = await Vote.get(id)
    users = [await User.get(id) for id in vote.users]
    return users
