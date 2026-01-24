from fastapi import APIRouter, status, Body, Path, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from app.schemas.users import UserCreateSchema, UserDataFromDbSchema
from app.core.database import get_db
from app.services.users_service import create_user_service, get_user_by_id_or_404



router = APIRouter(
    prefix="/users",
    tags=["users"]
)

#===============================#
#====== CRUD ===================#
#===============================#

# DETAIL by ID:
@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserDataFromDbSchema)
async def detail_user_by_id(
    user_id: Annotated[int, Path(..., description="ID of the user you search")],
    db: Annotated[Session, Depends(get_db)],
)->UserDataFromDbSchema:
    return get_user_by_id_or_404(id=user_id, db=db)

# CREATE:
@router.post("/", status_code=status.HTTP_201_CREATED, response_model= UserDataFromDbSchema)
async def create_user(
    user_fields: Annotated[UserCreateSchema, Body(...,description="Fields of new user")],
    db: Annotated[Session, Depends(get_db)],
)->UserDataFromDbSchema:
    return create_user_service(data=user_fields, db=db)
    