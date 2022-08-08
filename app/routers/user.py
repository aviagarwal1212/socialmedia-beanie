from app.models.user import OutUser, User
from app.utils import oauth2
from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OutUser)
async def create_user(user_data: User):
    hashed_password = oauth2.hash(user_data.password)
    user_data.password = hashed_password
    user = await User.insert_one(user_data)
    return user


@router.get("/{id}", response_model=OutUser)
async def get_user(id: PydanticObjectId):
    user = await User.get(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    return user
