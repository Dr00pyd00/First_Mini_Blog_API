from app.core.database import get_db
from app.schemas.post import PostDataFromDbSchema, PostDataToCreateSchema
from app.models.post import PostModel
from app.errors_msg.post import error_post_not_found_by_id

from fastapi import APIRouter, Depends,status, Body, Path
from sqlalchemy.orm import Session
from typing import List, Annotated


router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

#===============================#
#====== CRUD ===================#
#===============================#


# ALL:
@router.get("/", status_code=status.HTTP_200_OK, response_model= List[PostDataFromDbSchema])
async def get_all_posts(db:Session=Depends(get_db)):
    posts = db.query(PostModel).all()
    return posts

# DETAIL by ID:
@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostDataFromDbSchema)
async def post_detail_by_id(
    post_id:int,
    db:Session=Depends(get_db)
):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        error_post_not_found_by_id(post_id)
    return post
    
# CREATE:
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostDataFromDbSchema)
async def create_post(
    post_fields: Annotated[PostDataToCreateSchema, Body()],
    db: Annotated[Session, Depends(get_db)],
):
    new_post = PostModel(**post_fields.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# DELETE by ID:
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post_by_id(
    post_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        error_post_not_found_by_id(post_id)
    db.delete(post)
    db.commit()
    return

# UPDATE by ID:
@router.put("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostDataFromDbSchema)
async def update_post_by_id(
    post_id: Annotated[int, Path()],
    db: Annotated[Session, Depends(get_db)],
    post_new_fields: Annotated[PostDataToCreateSchema, Body()],
):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        error_post_not_found_by_id(post_id)
    
    for k,v in post_new_fields.model_dump().items():
        setattr(post,k,v)
    
    db.commit()
    db.refresh(post)
    return post

